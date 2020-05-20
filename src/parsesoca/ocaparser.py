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

    @_('IF clauses THEN "{" statements "}"')
    def classifier(self, p):
        return p.clauses, p.statements

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

    @_('expr BETWEEN expr AND expr')
    def clause(self, p):
        return p.BETWEEN, p.expr0, p.expr1, p.expr2

    # TODO: This does not work when there are OR clauses.
    @_('"(" clauses ")"')
    def clause(self, p):
        return p.clauses

    @_('expr EQUALS expr')
    def clause(self, p):
        return "==", p.expr0, p.expr1

    @_('expr NOTEQUALS expr')
    def clause(self, p):
        return "!=", p.expr0, p.expr1

    @_('expr LESSEQUALS expr')
    def clause(self, p):
        return "<=", p.expr0, p.expr1

    @_('expr GREATEREQUALS expr')
    def clause(self, p):
        return ">=", p.expr0, p.expr1

    @_('expr QEQUALS expr')
    def clause(self, p):
        return "?=", p.expr0, p.expr1

    @_('"(" expr ")"')
    def expr(self, p):
        return "()", p.expr

    @_('value "+" expr')
    def expr(self, p):
        return "+", p.value, p.expr

    @_('value "-" expr')
    def expr(self, p):
        return "-", p.value, p.expr

    @_('value')
    def expr(self, p):
        return p.value

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

    @_('expr "<" expr')
    def clause(self, p):
        return "<", p.expr0, p.expr1

    @_('expr ">" expr')
    def clause(self, p):
        return ">", p.expr0, p.expr1

    # TODO: generalize to any type?
    @_('KEYWORD IS TSTRING')
    def clause(self, p):
        return "IS_TSTRING", p.KEYWORD

    @_('KEYWORD IS TUNDEFINED')
    def clause(self, p):
        return "IS_TUNDEFINED", p.KEYWORD

    # Always True
    @_('TRUE')
    def clause(self, p):
        return True

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('KEYWORD "=" value ";"')
    def statement(self, p):
        return "=", p.KEYWORD, p.value

    @_('organizers organizer')
    def organizers(self, p):
        return p.organizers + [p.organizer]

    @_('organizer')
    def organizers(self, p):
        return [p.organizer]

    @_('SELECT EXECUTE "(" keywordorrecipename ")" '
       'FROM caliborinput '
       'WHERE clauses GROUPBY keywords AS ASPART ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses, p.keywords)

    # With a minRet, ignore it.
    @_('MINRET "=" NUMBER ";" '
       'SELECT EXECUTE "(" keywordorrecipename ")" '
       'FROM caliborinput '
       'WHERE clauses GROUPBY keywords AS ASPART ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses, p.keywords)

    # With a minRet, ignore it.
    @_('MINRET "=" NUMBER ";" '
       'SELECT EXECUTE "(" keywordorrecipename ")" '
       'FROM caliborinput '
       'WHERE clauses GROUPBY keywords ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses, p.keywords)

    @_('SELECT EXECUTE "(" keywordorrecipename ")" '
       'FROM caliborinput '
       'WHERE clauses GROUPBY keywords ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses, p.keywords)

    @_('SELECT EXECUTE "(" keywordorrecipename ")" '
       'FROM caliborinput '
       'WHERE clauses ";"')
    def organizer(self, p):
        return ("EXECUTE", p.keywordorrecipename, p.clauses)

    @_('INPUTFILES')
    def caliborinput(self, p):
        return p.INPUTFILES

    @_('CALIBFILES')
    def caliborinput(self, p):
        return p.CALIBFILES

    @_('RAWFILES')
    def caliborinput(self, p):
        return p.RAWFILES

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

    # TODO: Allow for multiple recipes in one action? E.g. molecfit
    @_('ACTION keywordorrecipename "{" '
       'inputselects '
       'recipespec '
       'outputproducts '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.inputselects, p.recipespec, p.outputproducts

    # Action with recipe after outputproducts.
    @_('ACTION keywordorrecipename "{" '
       'inputselects '
       'outputproducts '
       'recipespec '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.inputselects, p.recipespec, p.outputproducts

    # Action without inputselects.
    @_('ACTION keywordorrecipename "{" '
       'recipespec '
       'outputproducts '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.recipespec, p.outputproducts

    # Action without outputproducts, is this allowed? This means that the
    # recipe does not produce anything.
    @_('ACTION keywordorrecipename "{" '
       'inputselects '
       'recipespec '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.inputselects, p.recipespec

    # Action with only a recipe name.
    @_('ACTION keywordorrecipename "{" '
       'recipespec '
       '"}"')
    def action(self, p):
        return p.keywordorrecipename, p.recipespec

    # Recipe without parameters. With ;
    @_('RECIPE RECIPENAME ";"')
    def recipespec(self, p):
        return p.RECIPENAME

    # Recipe with 0 parameters. No ;
    @_('RECIPE RECIPENAME "{" "}"')
    def recipespec(self, p):
        return p.RECIPENAME

    # Recipe with parameters. Without ;
    @_('RECIPE RECIPENAME "{" recipeparameters "}"')
    def recipespec(self, p):
        return p.RECIPENAME, p.recipeparameters

    @_('recipeparameters recipeparameter')
    def recipeparameters(self, p):
        return p.recipeparameters + [p.recipeparameter]

    @_('recipeparameter')
    def recipeparameters(self, p):
        return [p.recipeparameter]

    @_('STRING ";"')
    def recipeparameter(self, p):
        return p.STRING

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
        return ("ACTION", p.NUMBER0, p.NUMBER1, p.caliborinput)

    # inputselect with accidentally two minret/maxret, e.g. xsh_wkf
    @_('MINRET "=" NUMBER ";" '
       'MAXRET "=" NUMBER ";" '
       'MINRET "=" NUMBER ";" '
       'MAXRET "=" NUMBER ";" '
       'SELECT FILE AS KEYWORD '
       'FROM caliborinput WHERE clauses ";" ')
    def inputselect(self, p):
        return ("ACTION", p.NUMBER2, p.NUMBER3, p.caliborinput)

    # inputselect with only minret
    # TODO: moons_wkf does not have the ";" everywhere
    @_('MINRET "=" NUMBER ";" '
       'SELECT FILE AS KEYWORD '
       'FROM caliborinput WHERE clauses ";" ')
    def inputselect(self, p):
        return ("ACTION", p.NUMBER, 99, p.caliborinput)

    # inputselect without minret and maxret
    @_('SELECT FILE AS KEYWORD '
       'FROM caliborinput WHERE clauses ";" ')
    def inputselect(self, p):
        return ("ACTION", -99, 99, p.caliborinput)

    @_('outputproducts outputproduct')
    def outputproducts(self, p):
        return p.outputproducts + [p.outputproduct]

    @_('outputproduct')
    def outputproducts(self, p):
        return [p.outputproduct]

    @_('PRODUCT KEYWORD "{" statements "}" ')
    def outputproduct(self, p):
        return p.KEYWORD, p.statements

    def error(self, token):
        raise ValueError(token)
