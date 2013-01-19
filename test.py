import unittest
from lib.lexer import *
import io

class TestSequenceFunctions(unittest.TestCase):

    def test_comments(self): 
        self.stream = io.open("./sample/comments.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'hello'),	Token('ASSIGNMENT', '='),	Token('FLOATNUM', '.23'),
                Token('MULTOP', '/'),			Token('INTNUM', '2'),		Token('SEMICOLON', ';'),
                Token('IF', 'if'),				Token('OPENPAR', '('),		Token('IDENTIFIER', 'hello'),
                Token('RELOP', '=='),		    Token('FLOATNUM', '1.23'),	Token('BOOLOP', 'or'),
                Token('IDENTIFIER', 'hello'),	Token('RELOP', '>='),		Token('INTNUM', '2'),
                Token('BOOLOP', 'or'),		    Token('IDENTIFIER', 'hello'),Token('RELOP', '<'),
                Token('INTNUM', '0'),		    Token('BOOLOP', 'and'),		Token('IDENTIFIER', 'hello'),
                Token('RELOP', '<>'),	        Token('INTNUM', '1'),		Token('CLOSEPAR', ')'),
                Token('OPENCURLY', '{'),	    Token('IDENTIFIER', 'print'),Token('OPENPAR', '('),
                Token('IDENTIFIER', 'test'),	Token('CLOSEPAR', ')'),		Token('SEMICOLON', ';'),
                Token('CLOSECURLY', '}')])

    def test_numbers(self):
        self.stream = io.open("./sample/numbers.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('FLOATNUM', '0.23'),		Token('FLOATNUM', '.23'),	Token('FLOATNUM', '1.23'),
                Token('INTNUM', '123')])

    def test_punctuation(self):
        self.stream = io.open("./sample/punctuation.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('RELOP', '=='),			Token('ADDOP', '+'),		Token('OPENPAR', '('),
                Token('IF', 'if'),				Token('RELOP', '<>'),		Token('ADDOP', '-'),
                Token('CLOSEPAR', ')'),			Token('THEN', 'then'),		Token('RELOP', '<'),
                Token('MULTOP', '*'),			Token('OPENCURLY', '{'),	Token('ELSE', 'else'),
                Token('RELOP', '>'),		    Token('MULTOP', '/'),		Token('CLOSECURLY', '}'),
                Token('WHILE', 'while'),	    Token('RELOP', '<='),		Token('ASSIGNMENT', '='),
                Token('OPENSQUARE', '['),		Token('DO', 'do'),			Token('RELOP', '>='),
                Token('BOOLOP', 'and'),			Token('CLOSESQUARE', ']'),	Token('CLASS', 'class'),
                Token('SEMICOLON', ';'),		Token('NOT', 'not'),		Token('INTEGER', 'integer'),
                Token('COMMA', ','),			Token('BOOLOP', 'or'),		Token('REAL', 'real'),
                Token('PERIOD', '.'),			Token('READ', 'read'),		Token('WRITE', 'write'),
                Token('RETURN', 'return')])

    def getTokensFromStream(self, stream):
        tokens = []
        token = nextToken(stream)
        while token:
            tokens.append(token)
            token = nextToken(stream)
        return tokens

    def tearDown(self):
        self.stream.close()

if __name__ == '__main__':
    unittest.main()
