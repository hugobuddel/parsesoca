# -*- coding: utf-8 -*-
"""Test classification."""
import os
from pathlib import Path
from pprint import pprint

from parsesoca.ocalexer import OCALexer
from parsesoca.ocaparser import OCAParser

from .test_many import do_test_oca_file


def test_ocas():
    """Test many OCA files."""
    path_here = Path(__file__).resolve().parent
    do_test_oca_file(path_here / "ocas" / "foundproblems.oca")

