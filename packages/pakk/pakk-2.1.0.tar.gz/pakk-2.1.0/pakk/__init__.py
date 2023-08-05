"""Package for encrypting and packing files into a single pakk file.

This module contains utility classes and functions for encrypting several files into
a single packed file. Pakk files are invokable and easily decrypted and expanded, similar
to the functionality of a ZIP file that doesn't have any compression. Pakk uses AES's CBC
Mode for encryption.

Pakk files abide by this format:
    Header:
        Magic Number            - 8  bytes  format: >Q  constant: (49 73 50 61 6b 6b 65 64)
        Initialization Vector   - 16 bytes  format: >16s
        File Count              - 4  bytes  format: >I

    repeat for file:
        File Name/Path Length   - 2  bytes  format: >H
        File Name/Path          - n  bytes  format: >(n)s
        File Size               - 4  bytes  format: >I
        File Content            - n  bytes  format: >(n)s

Example:
    Keys should be AES-compatible and are typically bytes-like objects::
        import hashlib

        password = "kitty"
        key = hashlib.sha256(password.encode("utf-8")).digest()

    You can pakk a single file using :func:`pakk_files`, the key provided must be a bytes-like object::

        with open("./outputfile.pakk", "wb") as out_file:
            pakk_files(key, ["./some/file"], out_file)

    And to unpakk back into files, use :func:`unpakk_files`::

        unpakk_files(key, "./outputfile.pakk")

    If you want to invoke a pakks file without unpakking it into the original file structure, use :func:`unpakk`::

        with open("./outputfile.pakk", "rb") as in_file:
            pakk = unpakk(key, in_file)

        for key, blob in pakk.blobs.items():
            print(f"{key}: {blob.name}")

"""
import io
import os
import struct
import shutil
from pathlib import Path
from typing import List, Union
from Crypto import Random
from Crypto.Cipher import AES

# 49 73 50 61 6b 6b 65 64 in big endian
PAKK_MAGIC_NUMBER = 5292662366434714980

class PakkError(Exception):
    """Basic exception for errors raised by Pakk
    """

class FileDoesNotExistError(PakkError):
    """Attempted to pakk or unpakk a file or folder that does not exist.
    """

class InvalidOutputDestinationError(PakkError):
    """Attempted to pakk or unpakk file(s) to a base destination that is not a folder.
    """

class InvalidPakkError(PakkError):
    """Attempted to parse a file that is not a valid Pakk file.
    """

class PakkBlob:
    """A named stream of blob data, typically represents a single pakk file.

    Attributes:
        name (str): The preferrably unique but pronouncable name of the blob.
        size (int): The size of the blob in bytes.
        stream (:obj:`io.BufferedIOBase`): A buffered stream to the blob of data.
    """
    def __init__(self, name: str, size: int, stream: io.BufferedIOBase):
        self.name = name
        self.size = size
        self.stream = stream

    def __str__(self):
        return f"({self.name}, {self.size}, {self.get_data()})"

    def get_data(self) -> bytes:
        """Get all data in the blob's stream as a :obj:`bytes` object.

        Returns:
            bytes: the data read from the blob's stream.
        """
        self.stream.seek(0)

        return self.stream.read(self.size)

class Pakk:
    """A collection of blobs. Typically correlates to a pakk file.

    Attributes:
        blobs (:obj:`dict` of :obj:`str` to :obj:`PakkBlob`): a dictionary of blobs in this pakk where the key is each blob's name.
    """
    def __init__(self, blobs: List[PakkBlob]):
        self.blobs = {}
        for item in blobs:
            self.blobs[item.name] = item

    def __contains__(self, key):
        return self.has_blob(key)

    def has_blob(self, key: str) -> bool:
        """Check if there is a blob with certain name in this pakk.

        Args:
            key (str): The name to check for within this pakk's blobs dictionary.

        Returns:
            bool. True if a blob with a certain key exists. False otherwise.
        """
        return key in self.blobs

    def get_blob(self, key: str) -> PakkBlob:
        """Get a specific blob by name.

        Args:
            key (str): The name of the blob to get.

        Returns:
            :class:`PakkBlob`. The blob matching the specified name.
        """
        return self.blobs[key]

def pakk(key: bytes, data: List[PakkBlob], output: io.BufferedIOBase, chunksize=64*1024):
    """Encrypt and pakk an input :class:`list` of :class:`PakkBlob` into a single buffered output.

    .. note::

        Appends to the current position in the output stream.

    Args:
        key (bytes): the key to encrypt the incoming blobs with, using SHA256
        data (list of :class:`PakkBlob`): the blobs to encrypt and pakk into the output buffer
        output (:class:`io.BufferedIOBase`): the buffer to write the pakk file data to

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to write to the output buffer
    """
    init_vector = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, init_vector)
    file_count = len(data)

    # pack MagicNumber, InitializationVector, and FileCount into the output byte array
    output.write(struct.pack(f">Q{AES.block_size}sI", PAKK_MAGIC_NUMBER, init_vector, file_count))
    for item in data:
        file_name_bytes = item.name.encode("utf-8")

        # pack FileNameLength, FileName, and FileSize into the output byte array
        output.write(struct.pack(f">H{len(file_name_bytes)}sI", len(file_name_bytes), file_name_bytes, item.size))

        while True:
            chunk = item.stream.read(chunksize)
            # ensure that item always has a length that is a multiple of 16
            # because AES expects an object with a number of bytes that are
            # a multiple of 16.
            if not chunk:
                break
            elif len(chunk) % 16 != 0:
                chunk += b"\x00" * (16 - len(chunk) % 16)

            output.write(encryptor.encrypt(chunk))

def unpakk(key: bytes, data: io.BufferedIOBase, chunksize=24*1024) -> Pakk:
    """Unpakk and decrypt a buffered stream of pakk file data.

    .. note::

        Reads from the current position in the stream.

    Args:
        key (bytes): the key to decrypt the pakk blobs with, using SHA256
        data (:class:`io.BufferedIOBase`): the buffer to read pakk file data from

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to read from the data buffer

    Returns:
        :class:`Pakk`. The pakks blob info and decrypted blob data.
    """
    files = list()

    # we gotta start from the beginning of the stream
    data.seek(0)

    # unpack MagicNumber, InitializationVector, and FileCount from pakk blob
    magic_number, init_vector, file_count = struct.unpack(f">Q{AES.block_size}sI", data.read(struct.calcsize(f">Q{AES.block_size}sI")))
    if magic_number != PAKK_MAGIC_NUMBER:
        raise InvalidPakkError()

    decryptor = AES.new(key, AES.MODE_CBC, init_vector)
    for _ in range(file_count):
        # unpack FileNameLength so that we can further unpack the FileName, followed by FileSize
        file_name_length = struct.unpack(">H", data.read(struct.calcsize(">H")))[0]
        file_name, file_size = struct.unpack(f">{file_name_length}sI", data.read(struct.calcsize(f">{file_name_length}sI")))

        blob = PakkBlob(file_name.decode("utf-8"), file_size, io.BytesIO())

        # since pakked files are padded by 0x00 if their size isnt divisible by 16
        # we need to account for that padding here, by adding the difference in size
        # to the file_size, and using that padded file_size when reading chunks from
        # the file
        padded_file_size = file_size
        if padded_file_size % 16 != 0:
            padded_file_size += (16 - padded_file_size % 16)

        # read the input chunk by chunk
        accumulated_size = 0
        while accumulated_size < padded_file_size:
            if padded_file_size < (accumulated_size + chunksize):
                chunk = data.read(padded_file_size - accumulated_size)
            else:
                chunk = data.read(chunksize)

            blob.stream.write(decryptor.decrypt(chunk))
            accumulated_size += chunksize

        blob.stream.truncate(file_size)

        files.append(blob)

    return Pakk(files)

def pakk_bytes(key, data: List[bytes], output: io.BufferedIOBase):
    """Encrypt and pakk an input :class:`list` of :class:`bytes` into a single buffered output.

    .. note::

        Appends to the current position in the output stream.

    Args:
        key (bytes): the key to encrypt the incoming blobs with, using SHA256
        data (list of :class:`bytes`): the bytes objects to encrypt and pakk into the output buffer
        output (:class:`io.BufferedIOBase`): the buffer to write the pakk file data to

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to write to the output buffer
    """

    init_vector = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, init_vector)
    file_count = len(data)

    # pack MagicNumber, InitializationVector, and FileCount into the output byte array
    output.write(struct.pack(f">Q{AES.block_size}sI", PAKK_MAGIC_NUMBER, init_vector, file_count))
    for index, item in enumerate(data):
        file_name_bytes = str(index).encode("utf-8")

        # pack FileNameLength, FileName, and FileSize into the output byte array
        output.write(struct.pack(f">H{len(file_name_bytes)}sI", len(file_name_bytes), file_name_bytes, len(item)))

        # ensure that item always has a length that is a multiple of 16
        # because AES expects an object with a number of bytes that are
        # a multiple of 16.
        if not item:
            break
        elif len(item) % 16 != 0:
            item += b"\x00" * (16 - len(item) % 16)

        output.write(encryptor.encrypt(item))

def unpakk_bytes(key, data: io.BufferedIOBase) -> List[bytes]:
    """Unpakk and decrypt a buffered stream of pakk file data into a list of bytes objects.

    .. note::

        Reads from the current position in the stream.

    Args:
        key (bytes): the key to decrypt the pakk blobs with, using SHA256
        data (:class:`io.BufferedIOBase`): the buffer to read pakk file data from

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to read from the data buffer

    Returns:
        list of bytes-objects. The decrypted blob data from the pakk file stream.
    """
    output = list()

    # we gotta start from the beginning of the stream
    data.seek(0)

    # unpack MagicNumber, InitializationVector, and FileCount from pakk blob
    magic_number, init_vector, file_count = struct.unpack(f">Q{AES.block_size}sI", data.read(struct.calcsize(f">Q{AES.block_size}sI")))
    if magic_number != PAKK_MAGIC_NUMBER:
        raise InvalidPakkError()

    decryptor = AES.new(key, AES.MODE_CBC, init_vector)
    for _ in range(file_count):
        # unpack FileNameLength so that we can further unpack the FileName, followed by FileSize
        file_name_length = struct.unpack(">H", data.read(struct.calcsize(">H")))[0]
        _, file_size = struct.unpack(f">{file_name_length}sI", data.read(struct.calcsize(f">{file_name_length}sI")))

        read_file_size = file_size
        if read_file_size == 0:
            output.append(bytes())
            break
        elif read_file_size % 16 != 0:
            read_file_size += (16 - read_file_size % 16)

        # decrypt, truncate ([:file_size]), and append our blob all in one line
        output.append(decryptor.decrypt(data.read(read_file_size))[:file_size])

    return output

def pakk_files(key, files: List[str], pakked_prefix: str, destination: Union[io.BufferedIOBase, str], chunksize=64*1024):
    """Encrypt and pakk specified files and folders into a single buffered output.

    .. note::

        Appends to the current position in the output stream.

    Args:
        key (bytes): the key to encrypt the incoming blobs with, using SHA256
        files (list of strings): the list of file and folders to encrypt and pakk
        pakked_prefix (string or None): the file prefix to remove from the pakked filenames
        destination (:class:`io.BufferedIOBase` or str): the buffer or file path to write the pakk file data to

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to write to the output buffer
    """
    init_vector = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, init_vector)

    # we use a set so that there are no duplicate file paths (dupe files is file).
    file_paths = set()
    for file in files:
        if os.path.isdir(file):
            # file is actually a folder path, not a file path
            # so lets walk the folder to get all files within it.
            for root, _, f_files in os.walk(file):
                for f_file in f_files:
                    file_paths.add(os.path.join(root, f_file))
        elif os.path.isfile(file):
            # its just a file path, so append it's to file_paths
            file_paths.add(file)
        else:
            raise FileDoesNotExistError()

    out_file = destination
    if isinstance(destination, str):
        out_file = open(destination, "wb")

    # magic number, initialization vector, and file count
    out_file.write(struct.pack(f">Q{AES.block_size}sI", PAKK_MAGIC_NUMBER, init_vector, len(file_paths)))

    for filename in file_paths:
        named_filename = filename
        if pakked_prefix:
            named_filename = filename[len(pakked_prefix):]
        filename_bytes = named_filename.encode("utf-8")

        # file name length, file name, and file size
        out_file.write(struct.pack(f">H{len(filename_bytes)}sI", len(filename_bytes), filename_bytes, os.path.getsize(filename)))

        with open(filename, "rb") as in_file:
            while True:
                chunk = in_file.read(chunksize)
                if not chunk:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b"\x00" * (16 - len(chunk) % 16)

                encrypted = encryptor.encrypt(chunk)
                out_file.write(encrypted)

    if isinstance(destination, str):
        out_file.close()

def unpakk_files(key, file: str, destination=os.curdir, chunksize=24*1024):
    """Unpakk and decrypt a pakk file at a specified path, writing the data into the original file structure at a specified root path.

    Args:
        key (bytes): the key to decrypt the pakk blobs with, using SHA256
        file (str): the path of the pakk file to unpakk and decrypt
        destination (str): the folder to output the unpakked files to

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to read from the data buffer
    """
    with open(file, "rb") as in_file:
        pakkfile = unpakk(key, in_file)

        blob: PakkBlob
        for key, blob in pakkfile.blobs.items():
            if os.path.isfile(destination):
                raise InvalidOutputDestinationError()

            blob.stream.seek(0)

            joined_dest = os.path.join(destination, blob.name)
            dirname = os.path.dirname(joined_dest)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # since pakked files are padded by 0x00 if their size isnt divisible by 16
            # we need to account for that padding here, by adding the difference in size
            # to the file_size, and using that padded file_size when reading chunks from
            # the file
            padded_file_size = blob.size
            if padded_file_size % 16 != 0:
                padded_file_size += (16 - padded_file_size % 16)

            # read the file chunk by chunk
            with open(joined_dest, "wb") as out_file:
                accumulated_size = 0
                while accumulated_size < padded_file_size:
                    if padded_file_size < (accumulated_size + chunksize):
                        chunk = blob.stream.read(padded_file_size - accumulated_size)
                    else:
                        chunk = blob.stream.read(chunksize)

                    out_file.write(chunk)
                    accumulated_size += chunksize

                out_file.truncate(blob.size)
