# pakk

Encrypt and pack several files or folders into a single invokable file.

This package comes equipped with a CLI tool and a simple library for working with pakk files. See the sections below regarding each.

## Getting Started

Pakk is built to work on Python 3.6 and above.

Install:
```sh
$ python3 -m pip install pakk
```

Using the CLI:
```sh
# pakk 'somefile.txt' and all the files in './somefolder' into 'files.pakk'
# encrypting with the password 'kitty'
$ pakk pakk -o files.pakk -p kitty somefile.txt ./somefolder

# unpakk 'files.pakk' into all the original files
$ pakk unpakk -o . -p kitty files.pakk
```

Using the library:
```py
import hashlib
import pakk

# encrypt with the password 'kitty'
password = "kitty"
key = hashlib.sha256(password.encode("utf-8")).digest()

# pakk 'somefile.txt' and all the files in './somefolder' into 'files.pakk'
with open("./files.pakk", "wb") as out_file:
    pakk_files(key, ["files.pakk", "./somefolder"], out_file)

# unpakk `files.pakk` into all the original files
unpakk_files(key, "./files.pakk")
```

## CLI

The pakk CLI tool has two subcommands: `pakk` and `unpakk`. Here are their help outputs:

```
$ pakk pakk --help
usage: pakk pakk [-h] [-o OUTPUT] [-p PASSWORD] [-c CHUNKSIZE] input

Encrypts the contents of a specified folder and packs the encrypted content
into a single pakk.

positional arguments:
  input                 input folder to encrypt and pakk.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output path of the pakk file.
  -p PASSWORD, --password PASSWORD
                        password used to encrypt the contents of the pakk.
                        Defaults to 'IsPakked'. It is HIGHLY recommended that
                        you supply your own secure password with high entropy
                        for each pakk.
  -c CHUNKSIZE, --chunksize CHUNKSIZE
                        maximum amount of bytes to encrypt at once when
                        pakking files in the folder. Must be an integer
                        multiple of 1024. Defaults to 64*1024
```

```
$ pakk unpakk --help
usage: pakk unpakk [-h] [-o OUTPUT] [-p PASSWORD] [-c CHUNKSIZE] input

Decrypts the contents of a specified pakk and unpacks it into an identical
folder structure as was originally packed.

positional arguments:
  input                 input pakk file to decrypt and unpakk.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        path of the folder to output the pakk contents to.
  -p PASSWORD, --password PASSWORD
                        password used to decrypt the contents of the pakk.
                        Must be the same password used when the pakk was
                        created, otherwise decryption will fail. Defaults to
                        'IsPakked'. It is HIGHLY recommended that you supply
                        your own secure password with high entropy for each
                        pakk.
  -c CHUNKSIZE, --chunksize CHUNKSIZE
                        maximum amount of bytes to decrypt at once when
                        unpakking files in the folder. Must be an integer
                        multiple of 1024. Defaults to 24*1024
```

## Library

pakk provides a [few functions and types](#API) for working with pakk buffers and files. In most use cases, `pakk_files` and `unpakk` are used to create pakk files and access data from pakk files.

### Example

Keys should be AES-compatible and are typically bytes-like objects:
```py
import hashlib

password = "kitty"
key = hashlib.sha256(password.encode("utf-8")).digest()
```

You can pakk a single file using `pakk_files`:
```py
with open("./outputfile.pakk", "wb") as out_file:
    pakk_files(key, ["./some/file"], out_file)
```

And to unpakk back into files, use `unpakk_files`:
```py
unpakk_files(key, "./outputfile.pakk")
```

If you want to invoke a pakks file without unpakking it into the original file structure, use `unpakk`:
```py
with open("./outputfile.pakk", "rb") as in_file:
    pakk = unpakk(key, in_file)

for key, blob in pakk.blobs.items():
    print(f"{key}: {blob.name}")
```

### API

```py
class PakkBlob:
    """A named stream of blob data, typically represents a single pakk file.

    Attributes:
        name (str): The preferrably unique but pronouncable name of the blob.
        size (int): The size of the blob in bytes.
        stream (:obj:`io.BufferedIOBase`): A buffered stream to the blob of data.
    """

class Pakk:
    """A collection of blobs. Typically correlates to a pakk file.

    Attributes:
        blobs (:obj:`dict` of :obj:`str` to :obj:`PakkBlob`): a dictionary of blobs in this pakk where the key is each blob's name.
    """

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

def pakk_files(key, files: List[str], destination: Union[io.BufferedIOBase, str], chunksize=64*1024):
    """Encrypt and pakk specified files and folders into a single buffered output.

    .. note::

        Appends to the current position in the output stream.

    Args:
        key (bytes): the key to encrypt the incoming blobs with, using SHA256
        files (list of strings): the list of file and folders to encrypt and pakk
        destination (:class:`io.BufferedIOBase` or str): the buffer or file path to write the pakk file data to

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to write to the output buffer
    """

def unpakk_files(key, file: str, destination=os.curdir, chunksize=24*1024):
    """Unpakk and decrypt a pakk file at a specified path, writing the data into the original file structure at a specified root path.

    Args:
        key (bytes): the key to decrypt the pakk blobs with, using SHA256
        file (str): the path of the pakk file to unpakk and decrypt
        destination (str): the folder to output the unpakked files to

    Kwargs:
        chunksize (int): the max size, in bytes, of the chunks to read from the data buffer
    """
```
