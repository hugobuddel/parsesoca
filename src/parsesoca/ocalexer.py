# -*- coding: utf-8 -*-

from sly import Lexer


class OCALexer(Lexer):
    """Lexer for OCA files."""

    # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
    tokens = {
        IF,
        KEYWORD,
        EQUALITY,
        STRING,
        AND,
        ASSIGNMENT,
        LIKE,
        SEMICOLON,
        THEN,
        LBRACE,
        RBRACE,
    }

    IF = r'if'
    KEYWORD = r'[A-Z\.]+'
    EQUALITY = r'=='
    STRING = r'"[A-Z%_]+"'
    AND = r'and'
    ASSIGNMENT = r'='
    LIKE = r'like'
    SEMICOLON = r';'
    THEN = r'then'
    LBRACE = r'{'
    RBRACE = r'}'

    ignore = ' \t'
    ignore_newline = r'\n+'

    def error(self, t):
        print(f"Illegal character {t.value[0]} at line {t.lineno}, character {t.index}.")
        self.index += 1
