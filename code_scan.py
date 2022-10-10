#!/usr/bin/python3

import argparse
import os
import re
from pathlib import Path


SCAN_DIR = Path(__file__).resolve(strict=True).parent


# PHP Insecure Functions: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/php-tricks-esp/php-useful-functions-disable_functions-open_basedir-bypass#php-code-execution
# PHP Security: https://www.acunetix.com/websitesecurity/php-security-2/
PHP_PATTERNS = [
    'shell_exec(',
    'system(',
    'exec(',
    'popen(',
    'passthru(',
    'proc_open(',
    'pcntl_exec(',
    'eval(',
    'assert(',
    'preg_replace(',    # This is only vulnerable if /e is in the expressions, because that triggers an eval() call
    'include(',
    'include_once(',
    'require(',
    'require_once(',
    "$_GET[",
    "= new Reflection",
    'InvokeArgs(array(',
    # need to check for common serialize/unserialize functions
]




def check_string_in_file(file_name, search_strings):
    """ Check if the provided strings are in the provided file and return back a list of lines that match.

        return <results_list>   a list of 2-tuples (line_number, line text)
    """
    line_number = 0
    results_list = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if isinstance(search_strings, list):
                for pattern in search_strings:
                    if pattern in line:
                        results_list.append((file_name, line_number, line.rstrip()))
            elif search_strings in line:
                # Assert a single string was passed since it wasn't a list type and just search once in the file
                results_list.append((line_number, line.rstrip()))
    return results_list


def check_string_in_file_advanced(file_name, search_strings, extra_lines=2):
    """ Check if the provided strings are in the provided file and return back a list of lines that match.

        return <results_list>   a list of 2-tuples (line_number, line text)
    """
    line_number = 0
    results_list = []
    with open(file_name, 'r') as read_obj:
        lines = read_obj.readlines()
    r = re.compile(r'exec\(')
    for i in range(len(lines)):
        if r.search(lines[i]):
            print("\n\nLine: {0}\n{1}".format(lines[i], '\n'.join(lines[max(0, i-2):i+2])))

    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if isinstance(search_strings, list):
                for pattern in search_strings:
                    if pattern in line:
                        results_list.append((file_name, line_number, line.rstrip()))
            elif search_strings in line:
                # Assert a single string was passed since it wasn't a list type and just search once in the file
                results_list.append((line_number, line.rstrip()))
    return results_list


def main():
    # argparse here
    parser = argparse.ArgumentParser(description="Code review file scanner for insecure patterns")
    parser.add_argument('-d', '--dir', action='store',
                        help='Directory to recursively scan below for files and patterns')
    parser.add_argument('-t', '--type', dest='file_type', action='store', required=False,
                        help='Specify file extension of file types you wish to scan for (e.g. php, jar, java)')
    parser.add_argument('--extra', required=False, help='Number of lines before/after to also print (default 2)')
    args = parser.parse_args()

    # walk tree down and find all .php files here and below
    files_to_scan = []
    results = []
    scan_for_type = "." + args.file_type if args.file_type else ".php"
    extras = int(args.extra) if args.extra else None
    for root, dirs, files in os.walk(SCAN_DIR):
        for file in files:
            if file.endswith(".php"):
                files_to_scan.append(os.path.join(root, file))
                results = check_string_in_file_advanced(os.path.join(root, file), PHP_PATTERNS)
    print("Found {} files with the desired file extension to analyze".format(len(files_to_scan)))
    if results:
        print("\nResults were found after scanning the provided path, please review them:")
        print("-" * 50)
        for r in results:
            print(f"File: {r[0]}\nLine: {r[1]} : {r[2]}\n\n")
        print("-" * 50)
    else:
        print("Sorry, no matching patterns were found in the provided path")
    return



if __name__ == '__main__':
    main()
