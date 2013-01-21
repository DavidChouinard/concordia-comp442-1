
from __future__ import print_function

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
                            return CompileError('Multiline comment is missing a matching close symbol ("*/")', stream)

                    character = stream.read(1)
                    if not character:
                        return CompileError('Multiline comment is missing a matching close symbol ("*/")', stream)
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
                if lexeme.upper() in ["IF", "THEN", "ELSE", "WHILE", "DO", "CLASS", "NOT", "INTEGER", "REAL", "READ", "WRITE", "RETURN"]:
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
                # we're dealing with a floating point number
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
                    stream.seek(stream.tell() - 1)
                    return CompileError('Unrecognized number format for "' + lexeme + '"', stream)
        else:
            # This is for unrecognized punctuation, weird control characters, etc.
            return CompileError('Unrecognized character "' + character + '"', stream)

class Token:
    # Tokens are internally stored as strings

    def __init__(self, token, lexeme):
        self.token = token.upper()
        self.lexeme = lexeme

    def __str__(self):
        return self.token + "='" + self.lexeme + "'"

    def __eq__(self, other):
        return (self.token == other.token and self.lexeme == other.lexeme)

class CompileError:
    # Tokens are internally stored as strings

    def __init__(self, message, stream):
        self.message = message

        if isinstance(stream, int):
            # This is for unit testing, it means stream is a line number
            self.line_number = stream
        else:
            self.stream = stream
            self.stream_position = stream.tell()

            # Start from the beginning and get the line number and context
            stream.seek(0)
            self.context = stream.readline()
            self.line_number = 1
            while stream.tell() < self.stream_position:
                self.context = stream.readline().strip()
                self.line_number += 1

            # Return stream position to original
            self.stream.seek(self.stream_position)

    def __eq__(self, other):
        return (self.message == other.message and self.line_number == other.line_number)
