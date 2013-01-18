#! /usr/bin/python
# -*- coding: utf-8 -*-

# Terminal colors
from colorama import init, Fore, Back, Style
init()

from lib.lexer import *
import io

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("source", help="source file to tokenize")
parser.add_argument("-d", "--debug", action="store_true",
                    help="save the output to two files (errors and token list)")
args = parser.parse_args()

def main():
    stream = io.open(args.source)

    if args.debug:
        output = io.open("./output/tokens.txt", "w")
        error_log = io.open("./output/errors.txt", "w")

    errors = []

    token = nextToken(stream)
    while token:
        if isinstance(token, CompileError):
            errors.append(token)
        else:
            output.write(u'(' + str(token) + u') ')
            #print(Fore.GREEN + "( " + Fore.RESET + str(token) + Fore.GREEN + " )" + Fore.RESET)
        token = nextToken(stream)

    if errors:
        print(Back.RED + "Found " + str(len(errors)) + " error" + ("s" if len(errors) > 1 else "") + ":" + Style.RESET_ALL + "\n")
        for error in errors:
            print("    " + error.message + "\n    " + Fore.CYAN + "Line " + str(error.line_number) + ":" + Style.RESET_ALL + "  " + error.context + "\n")
    else:
        print(Back.GREEN + "Success" + Style.RESET_ALL + " Tokenization completed without errors")

    output.close()
    error_log.close()
    stream.close()

if __name__ == "__main__":
    main()
