#! /usr/bin/python
# -*- coding: utf-8 -*-

from lib.lexer import *
import unittest
import io

class TestSequenceFunctions(unittest.TestCase):

    def test_ta_sample(self): 
        self.stream = io.open("./sample/ta_sample.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('CLASS', 'class'),		Token('IDENTIFIER', 'myClass'),Token('OPENCURLY', '{'),
                Token('INTEGER', 'integer'),	Token('IDENTIFIER', 'i'),	Token('ASSIGNMENT', '='),
                Token('INTNUM', '2'),			Token('SEMICOLON', ';'),	Token('REAL', 'real'),
                Token('ASSIGNMENT', '='),		Token('FLOATNUM', '6.99'),	Token('SEMICOLON', ';'),
                Token('IF', 'if'),				Token('OPENPAR', '('),		Token('IDENTIFIER', 'i'),
                Token('RELOP', '<='),			Token('INTNUM', '4'),		Token('CLOSEPAR', ')'),
                Token('OPENCURLY', '{'),		Token('CLOSECURLY', '}'),	Token('CLOSECURLY', '}')])

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

    def test_comments_unbalanced(self): 
        self.stream = io.open("./sample/comments_unbalanced.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'foo'),	Token('ASSIGNMENT', '='),	Token('FLOATNUM', '1.23'),
                Token('SEMICOLON', ';'), CompileError('Multiline comment is missing a matching close symbol ("*/")', 3)])

    def test_nested_comments(self): 
        self.stream = io.open("./sample/nested_comments.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'foo'),	Token('ASSIGNMENT', '='),	Token('FLOATNUM', '1.23'),
                Token('SEMICOLON', ';')])

    def test_comments_unbalanced2(self): 
        self.stream = io.open("./sample/comments_unbalanced2.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'foo'),	Token('ASSIGNMENT', '='),	Token('FLOATNUM', '1.23'),
                Token('SEMICOLON', ';'), CompileError('Multiline comment is missing a matching close symbol ("*/")', 3)])

    def test_numbers(self):
        self.stream = io.open("./sample/numbers.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('FLOATNUM', '0.23'),		Token('FLOATNUM', '.23'),	Token('FLOATNUM', '1.23'),
                Token('INTNUM', '123'),			CompileError('Unrecognized number format for "123."', 1),
                Token('FLOATNUM', '0.0'),		Token('INTNUM', '123'),		Token('IDENTIFIER', 'a')])

    def test_trailing_zeros(self):
        self.stream = io.open("./sample/trailing_zeros.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('FLOATNUM', '0.100000'),	Token('INTNUM', '00001')])

    def test_numbers_with_characters(self):
        self.stream = io.open("./sample/numbers_with_characters.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'i'),		Token('ASSIGNMENT', '='),	Token('INTNUM', '12'),
                Token('IF', 'if'),				Token('IDENTIFIER', 'i'),	Token('ASSIGNMENT', '='),
                Token('INTNUM', '12'),			Token('IF', 'if')])

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

    def test_unrecognized_characters(self):
        self.stream = io.open("./sample/unrecognized_characters.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('SEMICOLON', ';'),		Token('RELOP', '>='),		CompileError('Unrecognized character "|"', 1),
                Token('IDENTIFIER', 'foo'),		CompileError('Unrecognized character "~"', 1), Token('IDENTIFIER', 'bar')])

    def test_whitespace(self):
        self.stream = io.open("./sample/whitespace.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'foo'),	Token('NOT', 'not')])

    def test_keywords_at_start(self):
        self.stream = io.open("./sample/keywords_at_start.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
                [Token('IDENTIFIER', 'andfoo'),	Token('ASSIGNMENT', '='),	Token('INTNUM', '1'),
                Token('SEMICOLON', ';')])

    def test_identifiers(self):
        self.stream = io.open("./sample/identifiers.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
            [Token('IDENTIFIER', 'a'),			Token('IDENTIFIER', 'abc'),	Token('IDENTIFIER', 'abc123'),
            Token('IDENTIFIER', 'a1'),			Token('IDENTIFIER', 'a_'),	Token('IDENTIFIER', 'a123_'),
            CompileError('Unrecognized character "_"', 4), 	                Token('IDENTIFIER', 'ab'),
            Token('INTNUM', '123'),				Token('IDENTIFIER', 'ab')])

    def test_unicode(self):
        self.stream = io.open("./sample/unicode.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
            [Token('IDENTIFIER', u'téléphone'),	Token('ASSIGNMENT', '='),	Token('INTNUM', '45'),
            Token('SEMICOLON', ';'),			Token('IDENTIFIER', u'هاتف'),Token('ASSIGNMENT', '='),
            Token('INTNUM', '10'),				Token('SEMICOLON', ';')])

    def test_case(self):
        self.stream = io.open("./sample/case.txt")
        self.assertEqual(self.getTokensFromStream(self.stream),
            [Token('IF', 'if'),					Token('IF', 'if'),			Token('IDENTIFIER', 'foo'),
            Token('IDENTIFIER', 'FOO')])

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
