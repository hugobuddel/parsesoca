# -*- coding: utf-8 -*-
"""Test classification."""
import os
from pathlib import Path
from pprint import pprint

from parsesoca.ocalexer import OCALexer
from parsesoca.ocaparser import OCAParser


def cleanlines(lines):
    """Remove comments."""
    # TODO: refactor this in a general function
    in_comment = False
    for line in lines:
        if in_comment:
            if line.strip() == "*/":
                in_comment = False
        elif line.strip() == "/*":
            in_comment = True
        else:
            yield (line + "//")[:(line + "//").index("//")]


def do_test_oca_file(fn_oca):
    """Parse an OCA file."""
    print("do_test_oca_file", fn_oca)
    soca = open(fn_oca).read()

    soca_clean = "\n".join(
         line for line in cleanlines(soca.splitlines())
    )

    mylexer = OCALexer()
    # for token in mylexer.tokenize(soca_clean):
    #     print(token)

    myparser = OCAParser()
    myparser.parse(mylexer.tokenize(soca_clean))
    # pprint(myparser.parse(mylexer.tokenize(soca_clean)))
    if hasattr(myparser, 'errorok'):
        assert myparser.errorok, "Error"


def test_ocas():
    """Test many OCA files."""
    path_here = Path(__file__).resolve().parent
    for dirpath, _, filenames in os.walk(path_here):
        fns_oca = [fn for fn in filenames if fn.endswith(".oca")]
        fns_oca.sort(key=lambda fn: fn != 'foundproblems.oca')
        for fn_oca in fns_oca:
            print()
            print(fn_oca)
            do_test_oca_file(os.path.join(dirpath, fn_oca))

