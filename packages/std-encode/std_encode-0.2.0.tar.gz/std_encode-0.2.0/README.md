# std_encode

[![Build Status](https://travis-ci.org/jaimebuelta/std_encode.svg?branch=master)](https://travis-ci.org/jaimebuelta/std_encode)

Encode and decode files through standard input/output.

## Usage

Encode files piping them into `std_encode`

```
$ std_encode -t input_test.txt
>>>>>>>>>> START t input_test.txt
Some test
text file
<<<<<<<<<< END
```

The encoded text can be then decoded and saved with `std_decode`

```
$ std_encode -t input_test.txt | std_decode
######### DECODED FILE input_test.txt
$ cat input_test.txt
Some test
text file
```

## Install

The package is available in [PyPI](https://pypi.org/project/std-encode/)

    pip install std-encode


## Features

- A log shows that a file has been decoded
- Text and binary files are supported (binary are default).
- `std_decode` is capable of decoding more than one file in the same stream
- Any line in the stream that's not part of a file will be replicated in the standard output.

## Why is this useful for?

In some cases, standard input/output is a convenient and easy way of communication. Transfering a file is not as simple.

For example, the problem that originated it was to retrieve files from a docker container running in Kubernetes. Obtaining the text log is easy calling `docker logs` or `kubectl logs`, but retrieving files requires more plumbing.

In the operation, while creating logs, multiple files can be encoded, and then all will be retrieved piping the logs through `std_decode`, generating a resulting log like this one:

```
========================= test session starts ==========================
platform darwin -- Python 3.7.0, pytest-3.9.2, py-1.7.0, pluggy-0.8.0
rootdir: /Users/jaimebuelta/Dropbox/code/std_encode, inifile:
plugins: cram-0.2.0
collected 8 items

tests/base.t .                                                   [ 12%]
tests/double_file.t .                                            [ 25%]
tests/encode_decode_image.t .                                    [ 37%]
tests/encode_decode_text.t .                                     [ 50%]
tests/encode_image.t .                                           [ 62%]
tests/encode_text.t .                                            [ 75%]
tests/single_file.t .                                            [ 87%]
tests/test_se.py .                                               [100%]

======================= 8 passed in 2.22 seconds =======================

######### DECODED FILE junit_test.xml
######### DECODED FILE html_report.html
```
