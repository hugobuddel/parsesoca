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
        NOTEQUALS,
        LESSEQUALS,
        GREATEREQUALS,
        QEQUALS,
        LIKE,
        AND,
        OR,
        TRUE,
        IS,
        TSTRING,
        TUNDEFINED,

        SELECT,
        EXECUTE,
        FROM,
        WHERE,
        GROUPBY,
        AS,
        ASPART,
        INPUTFILES,
        CALIBFILES,
        RAWFILES,

        ACTION,
        MINRET,
        MAXRET,
        FILE,
        RECIPE,
        RECIPENAME,
        PRODUCT,
    }
    literals = {
        '=', '{', '}', ';', '<', '>', '(', ')', ',', '+', '-',
    }

    # A KEYWORD can also be a program name to execute.
    # And can also be used in action clauses, e.g.
    #   inputFile.INS.FILT1.NAME == INS.FILT1.NAME
    # "MJD-OBS" is also a keyword.
    # Perhaps this should be refactored?
    KEYWORD = r'(inputFile.)?(MJD-OBS|[A-Z][A-Z0-9\._]+)'
    IF = r'if'
    THEN = r'then'
    EQUALS = r'=='
    NOTEQUALS = r'!='
    LESSEQUALS = r'<='
    GREATEREQUALS = r'>='
    # TODO, what is ?= ?
    QEQUALS = r'\?='
    LIKE = r'like'
    AND = r'and'
    OR = r'or'
    IS = r'is'
    TSTRING = r'string'
    TUNDEFINED = r'undefined'

    SELECT = r'select'
    EXECUTE = r'execute'
    FROM = r'from'
    WHERE = r'where'
    GROUPBY = r'group[ ]+by'
    AS = r'as'
    # TODO: figure out what the AS clause actually means.
    ASPART = r'\(TPL_A,[ ]*(tpl|grp)\)'

    ACTION = r'action'
    MINRET = r'minRet'
    MAXRET = r'maxRet'
    FILE = r'file'
    # TODO: Perhaps refactor the input?
    INPUTFILES = r'inputFiles'
    CALIBFILES = r'calibFiles'
    RAWFILES = r'rawFiles'
    RECIPE = r'recipe'
    PRODUCT = r'product'
    RECIPENAME = r'[a-z][a-zA-Z0-9_]+'

    # TODO: Also do FALSE?
    TRUE = r'T'

    # From https://stackoverflow.com/a/12643073/2097
    @_(r'[+-]?([0-9]*[.])?[0-9]+')
    def NUMBER(self, t):
        # TODO: distinguish int and float?
        t.value = float(t.value)
        return t

    # = is only there for recipeparameters, perhaps refactor?
    @_(r'"[A-Za-z0-9%_\.,#/ =-]*"')
    def STRING(self, t):
        t.value = str(t.value.strip('"'))
        return t

    ignore = ' \t'
    ignore_newline = r'\n+'
