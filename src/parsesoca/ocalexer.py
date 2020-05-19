# -*- coding: utf-8 -*-

from sly import Lexer


# noinspection PyUnresolvedReferences,PyPep8Naming
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

        SELECT,
        EXECUTE,
        FROM,
        WHERE,
        GROUPBY,
        AS,
        ASPART,
        FILE,
    }
    literals = {
        '=', '{', '}', ';', '<', '>', '(', ')', ',',
    }

    # A KEYWORD can also be a program name to execute.
    KEYWORD = r'[A-Z\._]+'
    IF = r'if'
    THEN = r'then'
    EQUALS = r'=='
    LIKE = r'like'
    AND = r'and'

    SELECT = r'select'
    EXECUTE = r'execute'
    FROM = r'from'
    WHERE = r'where'
    GROUPBY = r'group[ ]+by'
    AS = r'as'
    # TODO: figure out what the AS clause actually means.
    ASPART = r'\(TPL_A,tpl\)'
    FILE = r'[a-z][a-zA-Z]+'

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
