# -*- coding: utf-8 -*-
"""Test classification."""

from pprint import pprint

from parsesoca.ocalexer import OCALexer
from parsesoca.ocaparser import OCAParser


def test_classification():
    """Test classification."""

    soca = """
    //CLASSIFICATION

    if DPR.CATG == "CALIB" and DPR.TECH == "IMAGE" and DPR.TYPE == "DARK"
      and INSTRUME like "%HAWKI%"
      and TPL.NEXP > 2 then
    {
      RAW.TYPE = "DARK";
      REFLEX.CATG = "DARK";
    }

    if PRO.CATG == "REFERENCE_DARK" and INSTRUME like "%HAWKI%" then
    {
      DO.CATG  = "REFERENCE_DARK";
      DO.CLASS = "REFERENCE_DARK";
      REFLEX.CATG = "REFERENCE_DARK";
    }

    select execute(DARKS) from inputFiles where RAW.TYPE=="DARK"
     group by DET.NCORRS.NAME,DET.DIT,DET.NDIT,TPL.START as (TPL_A,tpl);
    """

    soca_clean = "\n".join(
        line for line in soca.splitlines()
        if not (line.strip() + "//").startswith("//")
    )

    mylexer = OCALexer()
    for token in mylexer.tokenize(soca_clean):
        print(token)

    myparser = OCAParser()
    pprint(myparser.parse(mylexer.tokenize(soca_clean)))
