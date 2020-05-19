# -*- coding: utf-8 -*-
"""OCA Parser"""

from sly import Parser

from parsesoca.ocalexer import OCALexer


# noinspection PyUnresolvedReferences
class OCAParser(Parser):
    tokens = OCALexer.tokens

    def __init__(self):
        self.names = {}

    @_('classifiers organizers')
    def file(self, p):
        return p.classifiers, p.organizers

    @_('classifiers classifier')
    def classifiers(self, p):
        return p.classifiers + [p.classifier]

    @_('classifier')
    def classifiers(self, p):
        return [p.classifier]

    @_('IF clauses THEN "{" exprs "}"')
    def classifier(self, p):
        return p.clauses, p.exprs

    @_('clauses AND clause')
    def clauses(self, p):
        return p.clauses + [p.clause]

    @_('clause')
    def clauses(self, p):
        return [p.clause]

    @_('KEYWORD EQUALS value')
    def clause(self, p):
        return "==", p.KEYWORD, p.value

    @_('STRING')
    def value(self, p):
        return p.STRING

    @_('NUMBER')
    def value(self, p):
        return p.NUMBER

    @_('KEYWORD LIKE STRING')
    def clause(self, p):
        return "LIKE", p.KEYWORD, p.STRING

    @_('KEYWORD "<" NUMBER')
    def clause(self, p):
        return "<", p.KEYWORD, p.NUMBER

    @_('KEYWORD ">" NUMBER')
    def clause(self, p):
        return ">", p.KEYWORD, p.NUMBER

    @_('exprs expr')
    def exprs(self, p):
        return p.exprs + [p.expr]

    @_('expr')
    def exprs(self, p):
        return [p.expr]

    @_('KEYWORD "=" STRING ";"')
    def expr(self, p):
        return "=", p.KEYWORD, p.STRING

    @_('organizers organizer')
    def organizers(self, p):
        return p.organizers + [p.organizer]

    @_('organizer')
    def organizers(self, p):
        return [p.organizer]

    @_('SELECT EXECUTE "(" KEYWORD ")" FROM FILE WHERE clauses GROUPBY keywords AS ASPART ";"')
    def organizer(self, p):
        return ("EXECUTE", p.KEYWORD, p.FILE, p.clauses, p.keywords)

    @_('SELECT EXECUTE "(" KEYWORD ")" FROM FILE WHERE clauses GROUPBY keywords ";"')
    def organizer(self, p):
        return ("EXECUTE", p.KEYWORD, p.FILE, p.clauses, p.keywords)

    @_('keywords "," KEYWORD')
    def keywords(self, p):
        return p.keywords + [p.KEYWORD]

    @_('KEYWORD')
    def keywords(self, p):
        return [p.KEYWORD]
