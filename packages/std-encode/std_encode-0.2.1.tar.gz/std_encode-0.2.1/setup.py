# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['std_encode']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['std_decode = std_encode:console.run_sd',
                     'std_encode = std_encode:console.run_se']}

setup_kwargs = {
    'name': 'std-encode',
    'version': '0.2.1',
    'description': 'Encode and decode files through the standard input/output',
    'long_description': "# std_encode\n\n[![Build Status](https://travis-ci.org/jaimebuelta/std_encode.svg?branch=master)](https://travis-ci.org/jaimebuelta/std_encode)\n\nEncode and decode files through standard input/output.\n\n## Usage\n\nEncode files piping them into `std_encode`\n\n```\n$ std_encode -t input_test.txt\n>>>>>>>>>> START t input_test.txt\nSome test\ntext file\n<<<<<<<<<< END\n```\n\nThe encoded text can be then decoded and saved with `std_decode`\n\n```\n$ std_encode -t input_test.txt | std_decode\n######### DECODED FILE input_test.txt\n$ cat input_test.txt\nSome test\ntext file\n```\n\n## Install\n\nThe package is available in [PyPI](https://pypi.org/project/std-encode/)\n\n    pip install std-encode\n\n\n## Features\n\n- A log shows that a file has been decoded\n- Text and binary files are supported (binary are default).\n- `std_decode` is capable of decoding more than one file in the same stream\n- Any line in the stream that's not part of a file will be replicated in the standard output.\n\n## Why is this useful for?\n\nIn some cases, standard input/output is a convenient and easy way of communication. Transfering a file is not as simple.\n\nFor example, the problem that originated it was to retrieve files from a docker container running in Kubernetes. Obtaining the text log is easy calling `docker logs` or `kubectl logs`, but retrieving files requires more plumbing.\n\nIn the operation, while creating logs, multiple files can be encoded, and then all will be retrieved piping the logs through `std_decode`, generating a resulting log like this one:\n\n```\n========================= test session starts ==========================\nplatform darwin -- Python 3.7.0, pytest-3.9.2, py-1.7.0, pluggy-0.8.0\nrootdir: /Users/jaimebuelta/Dropbox/code/std_encode, inifile:\nplugins: cram-0.2.0\ncollected 8 items\n\ntests/base.t .                                                   [ 12%]\ntests/double_file.t .                                            [ 25%]\ntests/encode_decode_image.t .                                    [ 37%]\ntests/encode_decode_text.t .                                     [ 50%]\ntests/encode_image.t .                                           [ 62%]\ntests/encode_text.t .                                            [ 75%]\ntests/single_file.t .                                            [ 87%]\ntests/test_se.py .                                               [100%]\n\n======================= 8 passed in 2.22 seconds =======================\n\n######### DECODED FILE junit_test.xml\n######### DECODED FILE html_report.html\n```\n",
    'author': 'Jaime Buelta',
    'author_email': 'jaime.buelta@gmail.com',
    'url': 'https://github.com/jaimebuelta/std_encode',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
