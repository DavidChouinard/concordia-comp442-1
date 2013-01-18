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

    token = nextToken(stream)
    while token:
        print(Fore.GREEN + "( " + Fore.RESET + str(token) + Fore.GREEN + " )" + Fore.RESET, end=' ')
        token = nextToken(stream)

    stream.close()

    print()

    #print Fore.RED + 'some red text'
    #print Back.GREEN + 'and with a green background'
    #print Style.DIM + 'and in dim text'
    #print Fore.RESET + Back.RESET + Style.RESET_ALL
    #print 'back to normal now'

if __name__ == "__main__":
    main()
