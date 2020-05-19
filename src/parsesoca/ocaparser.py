# -*- coding: utf-8 -*-
"""OCA Parser"""

from sly import Parser

from parsesoca.ocalexer import OCALexer


# noinspection PyUnresolvedReferences
class OCAParser(Parser):
    tokens = OCALexer.tokens

    def __init__(self):
        self.names = {}

    @_('classifiers organizers actions')
    def file(self, p):
        return p.classifiers, p.organizers, p.actions

    # @_('classifiers organizers')
    # def file(self, p):
    #     return p.classifiers, p.organizers

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

    # TODO: treat OR differently than AND
    @_('clauses OR clause')
    def clauses(self, p):
        return p.clauses + [p.clause]

    @_('clause')
    def clauses(self, p):
        return [p.clause]

    # TODO: This does not work when there are OR clauses.
    @_('"(" clauses ")"')
    def clause(self, p):
        return p.clauses

    @_('KEYWORD EQUALS value')
    def clause(self, p):
        return "==", p.KEYWORD, p.value

    @_('STRING')
    def value(self, p):
        return p.STRING

    @_('NUMBER')
    def value(self, p):
        return p.NUMBER

    @_('KEYWORD')
    def value(self, p):
        return p.KEYWORD

    @_('KEYWORD LIKE STRING')
    def clause(self, p):
        return "LIKE", p.KEYWORD, p.STRING

    @_('KEYWORD "<" NUMBER')
    def clause(self, p):
        return "<", p.KEYWORD, p.NUMBER

    @_('KEYWORD ">" NUMBER')
    def clause(self, p):
        return ">", p.KEYWORD, p.NUMBER

    # TODO: generalize to any type?
    @_('KEYWORD IS TSTRING')
    def clause(self, p):
        return "IS_TSTRING", p.KEYWORD

    # Always True
    @_('TRUE')
    def clause(self, p):
        return True

    @_('exprs expr')
    def exprs(self, p):
        return p.exprs + [p.expr]

    @_('expr')
    def exprs(self, p):
        return [p.expr]

    @_('KEYWORD "=" value ";"')
    def expr(self, p):
        return "=", p.KEYWORD, p.value

    @_('organizers organizer')
    def organizers(self, p):
        return p.organizers + [p.organizer]

    @_('organizer')
    def organizers(self, p):
        return [p.organizer]

    @_('SELECT EXECUTE "(" keywordorrecipename ")" FROM caliborinput WHERE clauses GROUPBY keywords AS ASPART ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses, p.keywords)

    @_('SELECT EXECUTE "(" keywordorrecipename ")" FROM caliborinput WHERE clauses GROUPBY keywords ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses, p.keywords)

    @_('SELECT EXECUTE "(" keywordorrecipename ")" FROM caliborinput WHERE clauses ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses)

    @_('INPUTFILES')
    def caliborinput(self, p):
        return p.INPUTFILES

    @_('CALIBFILES')
    def caliborinput(self, p):
        return p.CALIBFILES

    @_('keywords "," KEYWORD')
    def keywords(self, p):
        return p.keywords + [p.KEYWORD]

    @_('KEYWORD')
    def keywords(self, p):
        return [p.KEYWORD]

    @_('actions action')
    def actions(self, p):
        return p.actions + [p.action]

    @_('action')
    def actions(self, p):
        return [p.action]

    @_('ACTION keywordorrecipename "{" '
       'inputselects '
       'RECIPE RECIPENAME ";" '
       'outputproducts '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.inputselects, p.RECIPENAME, p.outputproducts

    # Action without inputselects.
    @_('ACTION keywordorrecipename "{" '
       'RECIPE RECIPENAME ";" '
       'outputproducts '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.RECIPENAME, p.outputproducts

    # Action without outputproducts, is this allowed? This means that the
    # recipe does not produce anything.
    @_('ACTION keywordorrecipename "{" '
       'inputselects '
       'RECIPE RECIPENAME ";" '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.inputselects, p.RECIPENAME

    # Action with only a recipe name.
    @_('ACTION keywordorrecipename "{" '
       'RECIPE RECIPENAME ";" '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.RECIPENAME

    # actions can look like recipe names or like keywords....
    @_('KEYWORD')
    def keywordorrecipename(self, p):
        return p.KEYWORD

    @_('RECIPENAME')
    def keywordorrecipename(self, p):
        return p.RECIPENAME

    @_('inputselects inputselect')
    def inputselects(self, p):
        return p.inputselects + [p.inputselect]

    @_('inputselect')
    def inputselects(self, p):
        return [p.inputselect]

    @_('MINRET "=" NUMBER ";" '
       'MAXRET "=" NUMBER ";" '
       'SELECT FILE AS KEYWORD '
       'FROM caliborinput WHERE clauses ";" ')
    def inputselect(self, p):
        return ("ACTION", p.MINRET, p.NUMBER0, p.MAXRET, p.NUMBER1, p.caliborinput)

    @_('outputproducts outputproduct')
    def outputproducts(self, p):
        return p.outputproducts + [p.outputproduct]

    @_('outputproduct')
    def outputproducts(self, p):
        return [p.outputproduct]

    @_('PRODUCT KEYWORD "{" exprs "}" ')
    def outputproduct(self, p):
        return p.KEYWORD, p.exprs

    def error(self, token):
        raise ValueError(token)
