# -*- coding: utf-8 -*-
"""Test classification."""

from parsesoca.ocalexer import OCALexer
from parsesoca.ocaparser import OCAParser


def test_classification():
    """Test classification."""

    soca = """
    if PRO.CATG == "REFERENCE_DARK" and INSTRUME like "%HAWKI%" then
    {
      DO.CATG  = "REFERENCE_DARK";
      DO.CLASS = "REFERENCE_DARK";
      REFLEX.CATG = "REFERENCE_DARK";
    }
    """

    mylexer = OCALexer()
    for token in mylexer.tokenize(soca):
        print(token)

    myparser = OCAParser()
    print(myparser.parse(mylexer.tokenize(soca)))
