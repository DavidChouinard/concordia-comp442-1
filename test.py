#! /usr/bin/python
# -*- coding: utf-8 -*-

from lib.lexer import *
import unittest
import io

class TestSequenceFunctions(unittest.TestCase):

    def test_ta_sample(self): 
        self.stream = io.open("./sample/ta_sample.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('CLASS', 'class'),		Token.from_string('IDENTIFIER', 'myClass'),Token.from_string('OPENCURLY', '{'),
                Token.from_string('INTEGER', 'integer'),	Token.from_string('IDENTIFIER', 'i'),	Token.from_string('ASSIGNMENT', '='),
                Token.from_string('INTNUM', '2'),			Token.from_string('SEMICOLON', ';'),	Token.from_string('REAL', 'real'),
                Token.from_string('ASSIGNMENT', '='),		Token.from_string('FLOATNUM', '6.99'),	Token.from_string('SEMICOLON', ';'),
                Token.from_string('IF', 'if'),				Token.from_string('OPENPAR', '('),		Token.from_string('IDENTIFIER', 'i'),
                Token.from_string('RELOP', '<='),			Token.from_string('INTNUM', '4'),		Token.from_string('CLOSEPAR', ')'),
                Token.from_string('OPENCURLY', '{'),		Token.from_string('CLOSECURLY', '}'),	Token.from_string('CLOSECURLY', '}')])

    def test_comments(self): 
        self.stream = io.open("./sample/comments.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'hello'),	Token.from_string('ASSIGNMENT', '='),	Token.from_string('FLOATNUM', '.23'),
                Token.from_string('MULTOP', '/'),			Token.from_string('INTNUM', '2'),		Token.from_string('SEMICOLON', ';'),
                Token.from_string('IF', 'if'),				Token.from_string('OPENPAR', '('),		Token.from_string('IDENTIFIER', 'hello'),
                Token.from_string('RELOP', '=='),		    Token.from_string('FLOATNUM', '1.23'),	Token.from_string('BOOLOP', 'or'),
                Token.from_string('IDENTIFIER', 'hello'),	Token.from_string('RELOP', '>='),		Token.from_string('INTNUM', '2'),
                Token.from_string('BOOLOP', 'or'),		    Token.from_string('IDENTIFIER', 'hello'),Token.from_string('RELOP', '<'),
                Token.from_string('INTNUM', '0'),		    Token.from_string('BOOLOP', 'and'),		Token.from_string('IDENTIFIER', 'hello'),
                Token.from_string('RELOP', '<>'),	        Token.from_string('INTNUM', '1'),		Token.from_string('CLOSEPAR', ')'),
                Token.from_string('OPENCURLY', '{'),	    Token.from_string('IDENTIFIER', 'print'),Token.from_string('OPENPAR', '('),
                Token.from_string('IDENTIFIER', 'test'),	Token.from_string('CLOSEPAR', ')'),		Token.from_string('SEMICOLON', ';'),
                Token.from_string('CLOSECURLY', '}')])

    def test_comments_unbalanced(self): 
        self.stream = io.open("./sample/comments_unbalanced.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'foo'),	Token.from_string('ASSIGNMENT', '='),	Token.from_string('FLOATNUM', '1.23'),
                Token.from_string('SEMICOLON', ';'), CompileError('Multiline comment is missing a matching close symbol ("*/")', 3)])

    def test_nested_comments(self): 
        self.stream = io.open("./sample/nested_comments.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'foo'),	Token.from_string('ASSIGNMENT', '='),	Token.from_string('FLOATNUM', '1.23'),
                Token.from_string('SEMICOLON', ';')])

    def test_comments_unbalanced2(self): 
        self.stream = io.open("./sample/comments_unbalanced2.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'foo'),	Token.from_string('ASSIGNMENT', '='),	Token.from_string('FLOATNUM', '1.23'),
                Token.from_string('SEMICOLON', ';'), CompileError('Multiline comment is missing a matching close symbol ("*/")', 3)])

    def test_numbers(self):
        self.stream = io.open("./sample/numbers.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('FLOATNUM', '0.23'),		Token.from_string('FLOATNUM', '.23'),	Token.from_string('FLOATNUM', '1.23'),
                Token.from_string('INTNUM', '123'),			CompileError('Unrecognized number format for "123."', 1),
                Token.from_string('FLOATNUM', '0.0'),		Token.from_string('INTNUM', '123'),		Token.from_string('IDENTIFIER', 'a')])

    def test_trailing_zeros(self):
        self.stream = io.open("./sample/trailing_zeros.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('FLOATNUM', '0.100000'),	Token.from_string('INTNUM', '00001')])

    def test_numbers_with_characters(self):
        self.stream = io.open("./sample/numbers_with_characters.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'i'),		Token.from_string('ASSIGNMENT', '='),	Token.from_string('INTNUM', '12'),
                Token.from_string('IF', 'if'),				Token.from_string('IDENTIFIER', 'i'),	Token.from_string('ASSIGNMENT', '='),
                Token.from_string('INTNUM', '12'),			Token.from_string('IF', 'if')])

    def test_punctuation(self):
        self.stream = io.open("./sample/punctuation.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('RELOP', '=='),			Token.from_string('ADDOP', '+'),		Token.from_string('OPENPAR', '('),
                Token.from_string('IF', 'if'),				Token.from_string('RELOP', '<>'),		Token.from_string('ADDOP', '-'),
                Token.from_string('CLOSEPAR', ')'),			Token.from_string('THEN', 'then'),		Token.from_string('RELOP', '<'),
                Token.from_string('MULTOP', '*'),			Token.from_string('OPENCURLY', '{'),	Token.from_string('ELSE', 'else'),
                Token.from_string('RELOP', '>'),		    Token.from_string('MULTOP', '/'),		Token.from_string('CLOSECURLY', '}'),
                Token.from_string('WHILE', 'while'),	    Token.from_string('RELOP', '<='),		Token.from_string('ASSIGNMENT', '='),
                Token.from_string('OPENSQUARE', '['),		Token.from_string('DO', 'do'),			Token.from_string('RELOP', '>='),
                Token.from_string('BOOLOP', 'and'),			Token.from_string('CLOSESQUARE', ']'),	Token.from_string('CLASS', 'class'),
                Token.from_string('SEMICOLON', ';'),		Token.from_string('NOT', 'not'),		Token.from_string('INTEGER', 'integer'),
                Token.from_string('COMMA', ','),			Token.from_string('BOOLOP', 'or'),		Token.from_string('REAL', 'real'),
                Token.from_string('PERIOD', '.'),			Token.from_string('READ', 'read'),		Token.from_string('WRITE', 'write'),
                Token.from_string('RETURN', 'return')])

    def test_unrecognized_characters(self):
        self.stream = io.open("./sample/unrecognized_characters.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('SEMICOLON', ';'),		Token.from_string('RELOP', '>='),		CompileError('Unrecognized character "|"', 1),
                Token.from_string('IDENTIFIER', 'foo'),		CompileError('Unrecognized character "~"', 1), Token.from_string('IDENTIFIER', 'bar')])

    def test_whitespace(self):
        self.stream = io.open("./sample/whitespace.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'foo'),	Token.from_string('NOT', 'not')])

    def test_keywords_at_start(self):
        self.stream = io.open("./sample/keywords_at_start.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token.from_string('IDENTIFIER', 'andfoo'),	Token.from_string('ASSIGNMENT', '='),	Token.from_string('INTNUM', '1'),
                Token.from_string('SEMICOLON', ';')])

    def test_identifiers(self):
        self.stream = io.open("./sample/identifiers.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
            [Token.from_string('IDENTIFIER', 'a'),			Token.from_string('IDENTIFIER', 'abc'),	Token.from_string('IDENTIFIER', 'abc123'),
            Token.from_string('IDENTIFIER', 'a1'),			Token.from_string('IDENTIFIER', 'a_'),	Token.from_string('IDENTIFIER', 'a123_'),
            CompileError('Unrecognized character "_"', 4), 	                Token.from_string('IDENTIFIER', 'ab'),
            Token.from_string('INTNUM', '123'),				Token.from_string('IDENTIFIER', 'ab')])

    def test_unicode(self):
        self.stream = io.open("./sample/unicode.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
            [Token.from_string('IDENTIFIER', u'téléphone'),	Token.from_string('ASSIGNMENT', '='),	Token.from_string('INTNUM', '45'),
            Token.from_string('SEMICOLON', ';'),			Token.from_string('IDENTIFIER', u'هاتف'),Token.from_string('ASSIGNMENT', '='),
            Token.from_string('INTNUM', '10'),				Token.from_string('SEMICOLON', ';')])

    def test_case(self):
        self.stream = io.open("./sample/case.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
            [Token.from_string('IF', 'if'),					Token.from_string('IF', 'if'),			Token.from_string('IDENTIFIER', 'foo'),
            Token.from_string('IDENTIFIER', 'FOO')])

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
