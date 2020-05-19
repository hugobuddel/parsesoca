# -*- coding: utf-8 -*-

from sly import Lexer


class OCALexer(Lexer):
    """Lexer for OCA files."""

    # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
    tokens = {
        KEYWORD,
        STRING,
        NUMBER,
        IF,
        THEN,
        EQUALS,
        LIKE,
        AND,
    }
    literals = {
        '=', '{', '}', ';', '<', '>',
    }

    KEYWORD = r'[A-Z\.]+'
    IF = r'if'
    THEN = r'then'
    EQUALS = r'=='
    LIKE = r'like'
    AND = r'and'

    @_(r'[0-9]+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[A-Z%_]+"')
    def STRING(self, t):
        t.value = str(t.value.strip('"'))
        return t

    ignore = ' \t'
    ignore_newline = r'\n+'
