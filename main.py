#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Terminal colors
from colorama import init, Fore, Back, Style
init()

from lib.lexer import *
import io

def main():
    stream = io.open('./sample/1.txt')

    errors = []

    token = nextToken(stream)
    while token:
        if isinstance(token, CompileError):
            errors.append(token)
        #else:
            #print(Fore.GREEN + "( " + Fore.RESET + str(token) + Fore.GREEN + " )" + Fore.RESET, end=' ')
        token = nextToken(stream)

    if errors:
        print(Back.RED + "Found " + str(len(errors)) + " error" + ("s" if len(errors) > 1 else "") + ":" + Style.RESET_ALL + "\n")
        for error in errors:
            print("    " + error.message + "\n    " + Fore.CYAN + "Line " + str(error.line_number) + ":" + Style.RESET_ALL + "  " + error.context + "\n")
    else:
        print(Back.GREEN + "Success" + Style.RESET_ALL + " Tokenization completed without errors")

    stream.close()

if __name__ == "__main__":
    main()
