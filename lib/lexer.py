
from __future__ import print_function
from colorama import init, Fore, Back, Style

def nextToken(stream):
    while True:
        character = stream.read(1)
        if not character:
            # We reached the end of the file, our work here is done
            return None
        # Skip over all whitespace
        elif character.isspace():
            pass
        # Look for comments
        elif character == "/":
            # read the next character
            character = stream.read(1)
            if character == "/":
                # We found an inline comment, ignore all tokens until the next newline
                while character != "\n":
                    character = stream.read(1)
            elif character == "*":
                # We found a comment block, ignore all tokens until the next "*/"
                while True:
                    character = stream.read(1)
                    while character != "*":
                        character = stream.read(1)
                        if not character:
                            # TODO: We reached the end of the file without seeing a closed comment
                            print("Reached end of the file without seeing a closed comment symbol")
                            break

                    character = stream.read(1)
                    if not character:
                        # TODO: We reached the end of the file without seeing a closed comment
                        print("Reached end of the file without seeing a closed comment symbol")
                        break
                    if character == "/":
                        break
            else:
                # We saw a "/" but it isn't a comment, backtrack
                stream.seek(stream.tell() - 1)
                return Token("MULTOP", "/")
        elif character == ";":
            return Token("SEMICOLON", character)
        elif character == ",":
            return Token("COMMA", character)
        elif character == "+" or character == "-":
            return Token("ADDOP", character)
        elif character == "*":
            # Already dealt with division (see above)
            return Token("MULTOP", character)
        elif character == "(":
            return Token("OPENPAR", character)
        elif character == ")":
            return Token("CLOSEPAR", character)
        elif character == "[":
            return Token("OPENSQUARE", character)
        elif character == "]":
            return Token("CLOSESQUARE", character)
        elif character == "{":
            return Token("OPENCURLY", character)
        elif character == "}":
            return Token("CLOSECURLY", character)
        elif character == "=":
            # Read the following character
            if stream.read(1) == "=":
                return Token("RELOP", "==")
            else:
                # Oops, the next character is something else. It means we're dealing with
                # an assignment statement. Back off on character and return the token
                stream.seek(stream.tell() - 1)
                return Token("ASSIGNMENT", character)
        elif character == "<" or character == ">":
            next_character = stream.read(1)
            if next_character == "=" or (character == "<" and next_character == ">"):
                return Token("RELOP", character + next_character)
            else:
                stream.seek(stream.tell() - 1)
                return Token("RELOP", character)
        elif character.isalpha():
            # Find if we have an ID or an reserved keyword
            lexeme = ""
            while character.isalnum() or character == "_":
                # Reserved keywords
                lexeme += character
                if all(token is lexeme.upper() for token in ["IF", "THEN", "ELSE", "WHILE", "DO", "CLASS", "NOT", "INTEGER", "REAL" "READ", "WRITE", "RETURN"]):
                    return Token(lexeme.upper(), lexeme)
                elif lexeme.upper() == "OR" or lexeme.upper() == "AND":
                    return Token("BOOLOP", lexeme)
                character = stream.read(1)
            # If we reach here, we read one character too many (to make sure it
            # wasn't alpha-numeric). Backtrack one character.
            stream.seek(stream.tell() - 1)
            return Token("IDENTIFIER", lexeme)
        elif character.isdigit() or character == ".":

            if character == ".":
                next_character = stream.read(1)
                stream.seek(stream.tell() - 1)
                if not next_character.isdigit():
                    # We're dealing with a single period not a digit
                    return Token("PERIOD", character)

            #if character == "0":
                #next_character = stream.read(1)
                #stream.seek(stream.tell() - 1)

            lexeme = ""
            # TODO: deal with zero at beginning
            # if char == 0, only one level
            while character.isdigit():
                lexeme += character
                character = stream.read(1)

            if character != ".":
                # we're dealing with an integer
                stream.seek(stream.tell() - 1)
                return Token("INTNUM", lexeme)
            else:
                lexeme += character
                character = stream.read(1)

                # Check to make sure we don't have something of the form "123."
                if character.isdigit():
                    while character.isdigit():
                        lexeme += character
                        character = stream.read(1)
                    stream.seek(stream.tell() - 1)
                    return Token("FLOATNUM", lexeme)
                else:
                    # TODO: Throw error about "123." form
                    stream.seek(stream.tell() - 1)
        else:
            # TODO
            print(character, end='')

class Token:
    # Tokens are internally stored as strings

    def __init__(self, token, lexeme):
        self.token = token.upper()
        self.lexeme = lexeme

    def __str__(self):
        return self.token + "=" + self.lexeme
