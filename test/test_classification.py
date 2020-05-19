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

    select execute(DETECTOR_NOISE_COMPUTATION) from inputFiles where RAW.TYPE == "DARK" and DET.NDIT==1 group by ARCFILE;

    select execute(DARKS) from inputFiles where RAW.TYPE=="DARK"
     group by DET.NCORRS.NAME,DET.DIT,DET.NDIT,TPL.START as (TPL_A,tpl);

    action SKY_FLATS
    {
      // Select appropriate reference flat, if available
      minRet=0; maxRet=1;
      select file as REFERENCE_TWILIGHT_FLAT from inputFiles where
        REFLEX.CATG=="REFERENCE_TWILIGHT_FLAT"
        and inputFile.INS.FILT1.NAME==INS.FILT1.NAME
        and inputFile.INS.FILT2.NAME==INS.FILT2.NAME
        and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME;
      
      minRet = 1; maxRet = 1;
      select file as MASTER_DARK from calibFiles where
         PRO.CATG=="MASTER_DARK"
         and inputFile.DET.DIT==DET.DIT;

      recipe hawki_twilight_flat_combine;

      product MASTER_TWILIGHT_FLAT { PRO.CATG="MASTER_TWILIGHT_FLAT";}
      product MASTER_CONF { PRO.CATG="MASTER_CONF";}
      product MASTER_BPM { PRO.CATG="MASTER_BPM";}
      product RATIOIMG_TWILIGHT_FLAT {PRO.CATG="RATIOIMG_TWILIGHT_FLAT";}
      product RATIOIMG_STATS_TWILIGHT_FLAT {PRO.CATG="RATIOIMG_STATS_TWILIGHT_FLAT";}

    }
     
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
