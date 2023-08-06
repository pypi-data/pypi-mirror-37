# Azure Blob

[![PyPI version](https://badge.fury.io/py/azblob.svg)](https://badge.fury.io/py/azblob)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


One-line CLI to download from Azure blob storage. Supports private blobs.


## Installation

To install:

```
$ pip install azblob
```

## CLI

**Anonymous** access, account name from command line
```
$ azblob -n my_account download my_container my_blob
```
**Anonymous** access, account name from environment
```
$ export AZBLOB_ACCOUNTNAME=my_account
$ azblob download my_container my_blob
```

**Private** container, credentials from command line
```
$ azblob -n my_account -k my_key download my_container my_blob
```

**Private** container, credentials from environment
```
$ export AZBLOB_ACCOUNTNAME=my_account
$ export AZBLOB_ACCOUNTKEY=my_key
$ azblob download my_container my_blob
```

same principal (authenticatino)
```
azblob list my_container
```

and, as always
```
$ azblob -h
$ azblob download -h
```
