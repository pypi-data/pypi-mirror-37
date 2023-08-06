from __future__ import print_function
import os
import fileinput
import argparse
import base64

START_ENCODING = '>>>>>>>>>> START'
END_ENCODING = '<<<<<<<<<< END'


def run_sd():
    '''
    Read from the standard input to filter
    '''

    display = True
    mode = None
    for line in fileinput.input():
        if line.startswith(START_ENCODING):
            # Decode the start file
            mode_filename = line.split(START_ENCODING)[-1].strip()
            mode, filename = mode_filename.split()
            if mode == 'b':
                fp = open(filename, 'wb')
            elif mode == 't':
                fp = open(filename, 'w')
            else:
                raise Exception('Invalid mode {}'.format(mode))

            display = False
        elif line.startswith(END_ENCODING):
            print('######### DECODED FILE {}'.format(filename))
            display = True
            fp.close()
        elif display:
            print(line, end='')
        elif not display and mode == 'b':
            data = line.encode('ascii')
            data = base64.standard_b64decode(data)
            fp.write(data)
        elif not display and mode == 't':
            fp.write(line)
        else:
            raise Exception('Unexpected case')


def run_se():
    '''
    Read and dump a file with the proper format so it
    will be encoded back with se
    '''
    help_string = 'Encode a file in stdout. Recover it with std_decode'
    parser = argparse.ArgumentParser(description=help_string)
    parser.add_argument('file', type=argparse.FileType('rb'), help='file')
    parser.add_argument('-t', dest='text', action='store_true', default=False)

    args = parser.parse_args()
    filename = args.file.name
    mode = 'b'
    if args.text:
        mode = 't'
        args.file.close()
        args.file = open(filename, 'r')

    shortfilename = os.path.basename(filename)

    start_tmpl = '{start} {mode} {filename}'
    print(start_tmpl.format(start=START_ENCODING,
                            mode=mode,
                            filename=shortfilename))
    if mode == 't':
        for line in args.file:
            print(line, end='')
    elif mode == 'b':
        data = base64.standard_b64encode(args.file.read())
        print(data.decode('ascii'))

    print(END_ENCODING)
