#! /usr/bin/python
# -*- coding: utf-8 -*-

# Terminal colors
#from colorama import init, Fore, Back, Style
#init()

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
        elif args.debug:
            output.write(u'[' + str(token) + u'] ')

        token = nextToken(stream)

    if errors:
        #print(Back.RED + "Found " + str(len(errors)) + " error" + ("s" if len(errors) > 1 else "") + ":" + Style.RESET_ALL + "\n")
        print("Found " + str(len(errors)) + " error" + ("s" if len(errors) > 1 else "") + ":\n")

        if args.debug:
            error_log.write(u'Found ' + str(len(errors)) + u' error' + (u's' if len(errors) > 1 else u'') + u':\n\n')

        for error in errors:
            #print("    " + error.message + "\n    " + Fore.CYAN + "Line " + str(error.line_number) + ":" + Style.RESET_ALL + "  " + error.context)
            print("    " + error.message + "\n    Line " + str(error.line_number) + ":  " + error.context)

            if args.debug:
                error_log.write(u'    ' + error.message + u'\n    ' + u'Line ' + str(error.line_number) + u': ' + error.context + u'\n')
    else:
        #print(Back.GREEN + "Success!" + Style.RESET_ALL + " Tokenization completed without errors")
        print("Success! Tokenization completed without errors")
        if args.debug:
            error_log.write(u'Tokenization completed without errors')

    stream.close()

    if args.debug:
        output.close()
        error_log.close()

if __name__ == "__main__":
    main()
