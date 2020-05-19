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
        OR,

        SELECT,
        EXECUTE,
        FROM,
        WHERE,
        GROUPBY,
        AS,
        ASPART,
        INPUTFILES,
        CALIBFILES,

        ACTION,
        MINRET,
        MAXRET,
        FILE,
        RECIPE,
        RECIPENAME,
        PRODUCT,
    }
    literals = {
        '=', '{', '}', ';', '<', '>', '(', ')', ',',
    }

    # A KEYWORD can also be a program name to execute.
    # And can also be used in action clauses, e.g.
    #   inputFile.INS.FILT1.NAME == INS.FILT1.NAME
    # Perhaps this should be refactored?
    KEYWORD = r'[A-Z][A-Z0-9\._]+|inputFile.[A-Z][A-Z0-9\._]+'
    IF = r'if'
    THEN = r'then'
    EQUALS = r'=='
    LIKE = r'like'
    AND = r'and'
    OR = r'or'

    SELECT = r'select'
    EXECUTE = r'execute'
    FROM = r'from'
    WHERE = r'where'
    GROUPBY = r'group[ ]+by'
    AS = r'as'
    # TODO: figure out what the AS clause actually means.
    ASPART = r'\(TPL_A,tpl\)'

    ACTION = r'action'
    MINRET = r'minRet'
    MAXRET = r'maxRet'
    FILE = r'file'
    INPUTFILES = r'inputFiles'
    CALIBFILES = r'calibFiles'
    RECIPE = r'recipe'
    PRODUCT = r'product'
    RECIPENAME = r'[a-z][a-z0-9_]+'

    @_(r'[0-9]+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[A-Za-z0-9%_\.]+"')
    def STRING(self, t):
        t.value = str(t.value.strip('"'))
        return t

    ignore = ' \t'
    ignore_newline = r'\n+'
