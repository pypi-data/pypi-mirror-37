#!/usr/bin/env python
import sys
import json
import os
import time
import getopt
import browndog.bd as bd
import machine
from utils import *
from os.path import basename
from os.path import expanduser
from sys import stdin
from key_token import get_key_token


def main():
    """Command line interface to BD services."""
    bds = 'https://bd-api.ncsa.illinois.edu'

    # Important: This string has to be prepended to all informational messages printed by this program.
    # If not piping and redirection will not work properly.
    bdcli_str = "bdcli: "

    token_option = False
    verbose = False
    wait = 60
    output = ''
    list_outputs = False
    list_extractors = False
    find = False
    big_data = False
    token = ""
    metadata = []
    default_protocol = "https"
    auth_file_path = os.path.join(expanduser('~'), '.bdcli')  # Get auth file path

    try:
        # Arguments
        opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:w:vh', ['outputs', 'extractors', 'find', 'bigdata'])
    except getopt.GetoptError as err:
        print str(err)  # Print error message
        usage()  # Display usage
        sys.exit(2)

    for o, a in opts:
        if o == '-b':
            bds = a
            # Validating bds input
            if bds.find('://') == -1:
                bds = default_protocol + '://' + bds  # Use default protocol if none is provided
                print bdcli_str + 'No protocol provided. Changed URL to use the default protocol: ' + default_protocol
            else:
                protocol, server = bds.split('://')
                if not (protocol == "https" or protocol == "http"):
                    bds = default_protocol + '://' + server  # Set protocol to https if user provides other protocols
                    print bdcli_str + 'Invalid protocol provided. Changed URL to use the default protocol: ' + \
                        default_protocol + '.'
        elif o == '-t':
            token = a
            token_option = True
        elif o == '-v':
            verbose = True
        elif o == '-w':
            wait = int(a)
        elif o == '-h':
            usage()
            sys.exit()
        elif o == '-o':
            output = a
        elif o == '--outputs':
            list_outputs = True
        elif o == '--extractors':
            list_extractors = True
        elif o == '--find':
            find = True
        elif o == '--bigdata':
            big_data = True
        else:
            assert False, "unhandled option"

    print bdcli_str + 'Brown Dog API URL: ' + bds
    protocol, server = bds.split('://')  # Get protocol and server after all updates

    if token_option is False:
        # Get key token
        get_key_token(bds, auth_file_path)

        with open(auth_file_path, 'r') as f:
            auth_dict = json.load(f)
            token = auth_dict[server]['token']

    # Get input file
    if args:
        input_filename = args[0]
    else:
        input_filename = None
        # Iterate through the stdin messages
        for line in stdin:
            # Ignore all lines starting with bdcli_str
            if line is not None and line.startswith(bdcli_str) is False and line.startswith('\n') is False:
                # Read the first line that is not a message and then break from loop
                input_filename = line.split("\t")[0].strip()
                break

    # Download file if a URL
    if input_filename.startswith('http://') or input_filename.startswith('https://'):
        input_filename, status_code, status_text = bd.download_file(input_filename, '', token)

        # Something is not OK
        if not status_code == httplib.OK:
            process_common_http_status_codes(status_code, OP_FILE_DOWNLOAD)

    t0 = time.time()

    # Start docker machine for big data option
    is_docker_machine_started = False
    docker_machine = None
    if big_data:
        docker_machine = machine.Machine()
        # Start default docker machine if not already started
        if not docker_machine.exists():
            if verbose:
                print bdcli_str + 'Starting default docker machine'
            is_docker_machine_started = docker_machine.start()
        else:
            is_docker_machine_started = True

    # Carry out the data transformation
    if list_outputs:
        tmp, input_format = os.path.splitext(input_filename)
        input_format = input_format[1:]

        outputs, status_code, status_text = bd.outputs(bds, input_format, token)
        # Everything is OK
        if status_code == httplib.OK:
            print ', '.join(outputs)
        else:
            process_common_http_status_codes(status_code, OP_GET_OUTPUTS)
    elif list_extractors:
        tmp, input_format = os.path.splitext(input_filename)
        input_format = input_format[1:]

        extractors, status_code, status_text = bd.extractors(bds, input_format, token)
        # Everything is OK
        if status_code == httplib.OK:
            print extractors
        else:
            process_common_http_status_codes(status_code, OP_GET_EXTRACTORS)
    elif find:
        ranking, status_code, status_text = bd.find(bds, input_filename, token, wait)
        # Everything is OK
        if status_code == httplib.OK:
            ranking.pop(input_filename, None)  # Remove the query file if present

            if verbose:
                for filename in ranking:
                    print filename + ', ' + str(ranking[filename])

                print ''

            print min(ranking, key=ranking.get)  # Print out the most similar file
        else:
            process_common_http_status_codes(status_code, OP_FIND_SIMILAR)
    else:
        if output:
            if os.path.isdir(input_filename):
                directory = input_filename

                if not directory.endswith('/'):
                    directory += '/'

                for filename in os.listdir(directory):
                    if not filename[0] == '.' and not filename.endswith('.' + output) \
                            and not filename.endswith('.json'):
                        filename = directory + filename
                        output_filename = directory + os.path.splitext(basename(filename))[0] + '.' + output

                        if big_data:
                            if is_docker_machine_started:
                                output_filename, status_code, status_text = bd.convert_local(bds, filename, output,
                                                                                             output_filename, token,
                                                                                             docker_machine, wait,
                                                                                             verbose)
                                # Something is not OK
                                if not status_code == httplib.OK:
                                    process_common_http_status_codes(status_code, OP_FILE_CONVERSION_LOCAL)
                            else:
                                print bdcli_str + 'Docker machine not started. Please try again.'
                        else:
                            output_filename, status_code, status_text = bd.convert(bds, filename, output,
                                                                                   output_filename, token, wait,
                                                                                   verbose)
                            # Something is not OK
                            if not status_code == httplib.OK:
                                process_common_http_status_codes(status_code, OP_FILE_CONVERSION)

                output_filename = directory
            else:
                output_filename = os.path.splitext(basename(input_filename))[0] + '.' + output
                if big_data:
                    if is_docker_machine_started:
                        output_filename, status_code, status_text = bd.convert_local(bds, input_filename, output,
                                                                                     output_filename, token,
                                                                                     docker_machine, wait, verbose)
                        # Something is not OK
                        if not status_code == httplib.OK:
                            process_common_http_status_codes(status_code, OP_FILE_CONVERSION_LOCAL)
                    else:
                        print bdcli_str + 'Docker machine not started. Please try again.'
                else:
                    output_filename, status_code, status_text = bd.convert(bds, input_filename, output, output_filename,
                                                                           token, wait, verbose)
                    # Something is not OK
                    if not status_code == httplib.OK:
                        process_common_http_status_codes(status_code, OP_FILE_CONVERSION)

        elif os.path.isdir(input_filename):
            output_filename, status_code, status_text = bd.index(bds, input_filename, token, wait, verbose)
            # Something is not OK
            if not status_code == httplib.OK:
                process_common_http_status_codes(status_code, OP_FILE_INDEXING)
        else:
            if big_data:
                if is_docker_machine_started:
                    metadata, status_code, status_text = bd.extract_local(bds, input_filename, token, docker_machine,
                                                                          wait, verbose)
                    # Something is not OK
                    if not status_code == httplib.OK:
                        process_common_http_status_codes(status_code, OP_FILE_EXTRACTION_LOCAL)
                else:
                    print bdcli_str + 'Docker machine not started. Please try again.'
            else:
                metadata, status_code, status_text = bd.extract(bds, input_filename, token, wait=wait)
                # Everything is OK
                if status_code == httplib.OK:
                    metadata = json.dumps(metadata)
                else:
                    process_common_http_status_codes(status_code, OP_FILE_EXTRACTION)

            if verbose:
                print '\n' + bdcli_str + str(metadata) + '\n'

            # Write derived data to a file for later reference
            output_filename = os.path.splitext(os.path.basename(input_filename))[0] + '.json'

            with open(output_filename, 'w') as output_file:
                output_file.write(str(metadata))

        print(output_filename),

        if verbose:
            # Check for expected output
            if (os.path.isfile(output_filename) and os.stat(output_filename).st_size > 0) or os.path.isdir(
                    output_filename):
                print '\t\033[92m[OK]\033[0m'
            else:
                print '\t\033[91m[Failed]\033[0m'

    if verbose:
        dt = time.time() - t0
        print bdcli_str + 'Elapsed time: ' + time_to_string(dt)


def time_to_string(t):
    """Return a string representation of the give elapsed time"""
    h = int(t / 3600)
    m = int((t % 3600) / 60)
    s = int((t % 3600) % 60)

    if h > 0:
        return str(round(h + m / 60.0, 2)) + ' hours'
    elif m > 0:
        return str(round(m + s / 60.0, 2)) + ' minutes'
    else:
        return str(s) + ' seconds'


def usage():
    """Display README"""
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'HELP.txt')) as readme:
        print '\n' + readme.read().replace('\t\t', '  ')

if __name__ == '__main__':
    main()
