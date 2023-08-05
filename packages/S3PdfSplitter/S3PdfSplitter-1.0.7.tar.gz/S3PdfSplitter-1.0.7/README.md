# S3PdfSplitter [![Build Status](https://travis-ci.org/Nydareld/S3PdfSplitter.svg?branch=master)](https://travis-ci.org/Nydareld/S3PdfSplitter) [![Coverage Status](https://coveralls.io/repos/github/Nydareld/S3PdfSplitter/badge.svg)](https://coveralls.io/github/Nydareld/S3PdfSplitter) [![PyPI version](https://badge.fury.io/py/S3PdfSplitter.svg)](https://badge.fury.io/py/S3PdfSplitter) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/S3PdfSplitter.svg)

Python aws-s3 pdf spliter

## Usage

basic usage :

```python
from PdfSplitter import Splitter

spliter = Splitter("config.json")
spliter.split(data)
```

exemple config.json :
```json
{
    "aws" : {
        "access_key_id" : "aws-acces-key",
        "secret_access_key" : "aws secret",
    },
    "s3" : {
        "bucket" : "bucket"
    }
}
```
Note that the config is managed with [ConfigEnv](https://pypi.org/project/ConfigEnv/) so you can provide an .ini file or overide the config with environement variable ( AWS_S3_BUCKET, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY )

example data :
```json
{
    "input" : [
        "firstFile.pdf",
        "secondFile.pdf"
    ],
    "output": [
        {
            "s3Key": "output1.pdf",
            "pages": [
                { "index": 0, "pages": [0,1] },
                { "index": 1, "pages": [0,1] }
            ]
        },{
            "s3Key": "output2.pdf",
            "pages": [
                { "index": 0, "pages": [0] },
                { "index": 1, "pages": [0] },
                { "index": 0, "pages": [1] },
                { "index": 1, "pages": [1] }
            ]
        }
    ]
}
```

this will produce 2 pdfs in your s3:
 - the first, output1.pdf, with page 0 and 1 from firstFile and page 0 and 1 from secondFile
 - the second, output2.pdf, with page 0 from firstFile, page 0 from secondFile, page 1 from firstFile and page 1 from secondFile


## Developpement guide

### installation

with virtualenv :

    # create virtualenv
    virtualenv -p python3 .venv

    # activate venv
    source .venv/bin/activate

    # install dependancies
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

### testing

with unittest :

    # if your test config is setup :
    python -m unittest

    # if you want to overide your test config :
    S3_BUCKET=<your bucket> AWS_ACCESS_KEY_ID=<your key id> AWS_SECRET_ACCESS_KEY=<your key secret> python -m unittest
