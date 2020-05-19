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


if DPR.CATG == "CALIB" and DPR.TECH == "IMAGE" and DPR.TYPE == "FLAT"
  and INSTRUME like "%HAWKI%"
  and TPL.NEXP > 2 then
{
  RAW.TYPE = "FLAT_TWILIGHT";
  REFLEX.CATG = "FLAT_TWILIGHT";
}

if PRO.CATG == "REFERENCE_TWILIGHT_FLAT" and INSTRUME like "%HAWKI%" then
{
  DO.CATG  = "REFERENCE_TWILIGHT_FLAT";
  DO.CLASS = "REFERENCE_TWILIGHT_FLAT";
  REFLEX.CATG = "REFERENCE_TWILIGHT_FLAT";
}

if (DPR.CATG == "CALIB" or DPR.CATG == "TEST") and DPR.TECH == "IMAGE" and DPR.TYPE == "STD"
  and INSTRUME like "%HAWKI%"
//  and TPL.NEXP == 4
//  and (
//    INS.FILT1.NAME == "J" or
//    INS.FILT1.NAME == "H" or
//    INS.FILT1.NAME == "Ks" or
//    INS.FILT1.NAME == "Y"
//      ) and
//    INS.FILT2.NAME =="OPEN"
  then
{
  RAW.TYPE = "STD";
  REFLEX.CATG = "STD";
  REFLEX.TARGET="T";
}


if DPR.CATG == "SCIENCE" and DPR.TECH == "IMAGE" and DPR.TYPE == "OBJECT" 
 and INSTRUME like "%HAWKI%"
 then
{
  RAW.TYPE = "SCIENCE_IMG";
  DO.CATG = "OBJECT";
  PACK.DIR = "NONE";
  REFLEX.CATG = "OBJECT";
  REFLEX.TARGET = "T";
}

if DPR.CATG == "SCIENCE" and DPR.TECH == "IMAGE" and DPR.TYPE == "SKY" 
 and INSTRUME like "%HAWKI%"
 then
{
  RAW.TYPE = "SCIENCE_IMG";
  DO.CATG = "SKY";
  PACK.DIR = "NONE";
  REFLEX.CATG = "SKY";
  REFLEX.TARGET = "T";
}

if RFXNAME == "casu_2mass_astrom" then
{
  DO.CATG  = "MASTER_2MASS_CATALOGUE_ASTROM";
  DO.CLASS = "MASTER_2MASS_CATALOGUE_ASTROM";
  REFLEX.CATG = "MASTER_2MASS_CATALOGUE_ASTROM";
  PRO.CATG = "MASTER_2MASS_CATALOGUE_ASTROM";
}

if RFXNAME == "casu_2mass_photom" then
{
  DO.CATG  = "MASTER_2MASS_CATALOGUE_PHOTOM";
  DO.CLASS = "MASTER_2MASS_CATALOGUE_PHOTOM";
  REFLEX.CATG = "MASTER_2MASS_CATALOGUE_PHOTOM";
  PRO.CATG = "MASTER_2MASS_CATALOGUE_PHOTOM";
}

if RFXNAME == "casu_ppmxl_astrom" then
{
  DO.CATG  = "MASTER_PPMXL_CATALOGUE_ASTROM";
  DO.CLASS = "MASTER_PPMXL_CATALOGUE_ASTROM";
  REFLEX.CATG = "MASTER_PPMXL_CATALOGUE_ASTROM";
  PRO.CATG = "MASTER_PPMXL_CATALOGUE_ASTROM";
 }

if RFXNAME == "casu_ppmxl_photom" then
{
  DO.CATG  = "MASTER_PPMXL_CATALOGUE_PHOTOM";
  DO.CLASS = "MASTER_PPMXL_CATALOGUE_PHOTOM";
  REFLEX.CATG = "MASTER_PPMXL_CATALOGUE_PHOTOM";
  PRO.CATG = "MASTER_PPMXL_CATALOGUE_PHOTOM";
}

if RFXNAME == "casu_local_astrom" then
{
  DO.CATG  = "MASTER_LOCAL_CATALOGUE_ASTROM";
  DO.CLASS = "MASTER_LOCAL_CATALOGUE_ASTROM";
  REFLEX.CATG = "MASTER_LOCAL_CATALOGUE_ASTROM";
  PRO.CATG = "MASTER_LOCAL_CATALOGUE_ASTROM";
}

if RFXNAME == "casu_local_photom" then
{
  DO.CATG  = "MASTER_LOCAL_CATALOGUE_PHOTOM";
  DO.CLASS = "MASTER_LOCAL_CATALOGUE_PHOTOM";
  REFLEX.CATG = "MASTER_LOCAL_CATALOGUE_PHOTOM";
  PRO.CATG = "MASTER_LOCAL_CATALOGUE_PHOTOM";
}


if PRO.CATG == "PHOTCAL_TAB" then
{
  DO.CATG  = "PHOTCAL_TAB";
  DO.CLASS = "PHOTCAL_TAB";
  REFLEX.CATG = "PHOTCAL_TAB";
}

// do we need to match on anything else? INSTRUME?
if PRO.CATG == "MASTER_READGAIN" then
{
  DO.CATG  = "MASTER_READGAIN";
  DO.CLASS = "MASTER_READGAIN";
  REFLEX.CATG = "MASTER_READGAIN";
}


if PRO.CATG == "SCHLEGEL_MAP_NORTH" then
{
  DO.CATG  = "SCHLEGEL_MAP_NORTH";
  DO.CLASS = "SCHLEGEL_MAP_NORTH";
  REFLEX.CATG = "SCHLEGEL_MAP_NORTH";
}

if PRO.CATG == "SCHLEGEL_MAP_SOUTH" then
{
  DO.CATG  = "SCHLEGEL_MAP_SOUTH";
  DO.CLASS = "SCHLEGEL_MAP_SOUTH";
  REFLEX.CATG = "SCHLEGEL_MAP_SOUTH";
}


//ORGANIZATION


select execute(DARKS) from inputFiles where RAW.TYPE=="DARK"
  group by DET.NCORRS.NAME,DET.DIT,DET.NDIT,TPL.START as (TPL_A,tpl);

select execute(SKY_FLATS) from inputFiles where RAW.TYPE=="FLAT_TWILIGHT"
  group by DET.NCORRS.NAME,DET.DIT,DET.NDIT,INS.FILT1.NAME,INS.FILT2.NAME,OBS.START as (TPL_A,tpl);

select execute(DETECTOR_NOISE_COMPUTATION) from inputFiles where RAW.TYPE == "DARK" and DET.NDIT==1 group by ARCFILE;

select execute(STANDARD_STARS) from inputFiles where RAW.TYPE=="STD"
  group by DET.NCORRS.NAME,DET.DIT,DET.NDIT,INS.FILT1.NAME,INS.FILT2.NAME,OBS.TARG.NAME,OBS.START as (TPL_A,tpl);

select execute(SCIENCE_FRAMES) from inputFiles where RAW.TYPE=="SCIENCE_IMG"
  group by DET.NCORRS.NAME,DET.DIT,DET.NDIT,INS.FILT1.NAME,INS.FILT2.NAME,OBS.START as (TPL_A,tpl);


action DARKS
{
  minRet=0; maxRet=1;
  select file as REFERENCE_DARK from inputFiles where
    REFLEX.CATG=="REFERENCE_DARK"
    and inputFile.DET.DIT==DET.DIT
    and inputFile.DET.NDIT==DET.NDIT
    and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME;

  recipe hawki_dark_combine;

  product MASTER_DARK { PRO.CATG="MASTER_DARK";}
  product DIFFIMG_DARK { PRO.CATG="DIFFIMG_DARK";}
  product DIFFIMG_STATS_DARK { PRO.CATG="DIFFIMG_STATS_DARK";}

}


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

action DETECTOR_NOISE_COMPUTATION
{
  // the wkflw is designed to only pass CONF map; recipe says
  //  that only one of [BPM, CONF] are used
  minRet = 0; maxRet=1;
  select file as MASTER_BPM from calibFiles where
    PRO.CATG=="MASTER_BPM";

  // if using a CONF, it should be one with same filter as FLAT_TWILIGHT!
  minRet=0; maxRet=1;
  select file as MASTER_CONF from calibFiles where
    PRO.CATG=="MASTER_CONF";

  minRet=2; maxRet = 2;
  select file as DARK_NOISE from inputFiles where RAW.TYPE=="DARK" 
    and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME;

  minRet=2; maxRet = 2;
  select file as FLAT_TWILIGHT from inputFiles where RAW.TYPE=="FLAT_TWILIGHT";

  recipe hawki_detector_noise;
  
   product MASTER_READGAIN {
     PRO.CATG="MASTER_READGAIN_WKF";
     REFLEX.CATG="MASTER_READGAIN_WKF";
  }

}

action STANDARD_STARS
{

  minRet = 1; maxRet = 1;
  select file as MASTER_DARK from calibFiles where
     PRO.CATG=="MASTER_DARK"
     and inputFile.DET.DIT==DET.DIT;

  minRet = 1; maxRet = 1;
  select file as MASTER_TWILIGHT_FLAT from calibFiles where
     PRO.CATG=="MASTER_TWILIGHT_FLAT"
     and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME
     and (inputFile.INS.FILT1.NAME==INS.FILT1.NAME and inputFile.INS.FILT2.NAME==INS.FILT2.NAME);

  minRet = 1; maxRet = 1;
  select file as PHOTCAL_TAB from calibFiles where
     DO.CATG=="PHOTCAL_TAB";

  minRet = 1; maxRet = 1;
  select file as MASTER_CONF from calibFiles where
     PRO.CATG=="MASTER_CONF"
     and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME
     and (inputFile.INS.FILT1.NAME==INS.FILT1.NAME and inputFile.INS.FILT2.NAME==INS.FILT2.NAME);

  minRet = 0; maxRet = 1;
  select file as MASTER_READGAIN_WKF from calibFiles where
     (REFLEX.CATG=="MASTER_READGAIN_WKF");

  minRet = 1; maxRet = 1;
  select file as MASTER_READGAIN from calibFiles where
     (REFLEX.CATG=="MASTER_READGAIN") ;

  minRet = 0; maxRet = 1;
  select file as MASTER_2MASS_CATALOGUE_ASTROM from calibFiles where
     REFLEX.CATG =="MASTER_2MASS_CATALOGUE_ASTROM";
  minRet = 0; maxRet = 1;
  select file as MASTER_2MASS_CATALOGUE_PHOTOM from calibFiles where
     REFLEX.CATG =="MASTER_2MASS_CATALOGUE_PHOTOM";

  minRet = 0; maxRet = 1;
  select file as MASTER_PPMXL_CATALOGUE_ASTROM from calibFiles where
     REFLEX.CATG =="MASTER_PPMXL_CATALOGUE_ASTROM";
  minRet = 0; maxRet = 1;
  select file as MASTER_PPMXL_CATALOGUE_PHOTOM from calibFiles where
     REFLEX.CATG =="MASTER_PPMXL_CATALOGUE_PHOTOM";

  minRet = 0; maxRet = 1;
  select file as MASTER_LOCAL_CATALOGUE_ASTROM from calibFiles where
     REFLEX.CATG =="MASTER_LOCAL_CATALOGUE_ASTROM";
  minRet = 0; maxRet = 1;
  select file as MASTER_LOCAL_CATALOGUE_PHOTOM from calibFiles where
     REFLEX.CATG =="MASTER_LOCAL_CATALOGUE_PHOTOM";

  minRet = 1; maxRet = 1;
  select file as SCHLEGEL_MAP_NORTH from calibFiles where
     DO.CATG =="SCHLEGEL_MAP_NORTH";
  minRet = 1; maxRet = 1;
  select file as SCHLEGEL_MAP_SOUTH from calibFiles where
     DO.CATG =="SCHLEGEL_MAP_SOUTH";

  recipe hawki_standard_process;

  product BASIC_CALIBRATED_STD { PRO.CATG="BASIC_CALIBRATED_STD";}
  product BASIC_VAR_MAP_STD { PRO.CATG="BASIC_VAR_MAP";}  // note that product name != PRO.CATG
  product BASIC_CAT_STD { PRO.CATG="BASIC_CAT_STD";}
  product MEAN_SKY {PRO.CATG="MEAN_SKY";}
  product MEAN_SKY_VAR {PRO.CATG="MEAN_SKY_VAR";}
  product MATCHSTD_ASTROM {PRO.CATG="MATCHSTD_ASTROM";}  // one created for each input frame
  product MATCHSTD_PHOTOM {PRO.CATG="MATCHSTD_PHOTOM";}  // one created for each input frame

}

action SCIENCE_FRAMES
{
  minRet = 1; maxRet = 1;
  select file as MASTER_TWILIGHT_FLAT from calibFiles where
     PRO.CATG=="MASTER_TWILIGHT_FLAT"
     and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME
     and inputFile.INS.FILT1.NAME==INS.FILT1.NAME and inputFile.INS.FILT2.NAME==INS.FILT2.NAME;
  minRet = 1; maxRet = 1;
  select file as MASTER_CONF from calibFiles where
     PRO.CATG=="MASTER_CONF"
     and inputFile.DET.NCORRS.NAME==DET.NCORRS.NAME
     and inputFile.INS.FILT1.NAME==INS.FILT1.NAME and inputFile.INS.FILT2.NAME==INS.FILT2.NAME;

  minRet = 1; maxRet = 1;
  select file as MASTER_DARK from calibFiles where
     PRO.CATG=="MASTER_DARK"
     and inputFile.DET.DIT==DET.DIT;
  minRet = 1; maxRet = 1;
  select file as PHOTCAL_TAB from calibFiles where
     DO.CATG=="PHOTCAL_TAB";

  minRet = 0; maxRet = 1;
  select file as MASTER_READGAIN_WKF from calibFiles where
     (REFLEX.CATG=="MASTER_READGAIN_WKF");

  minRet = 1; maxRet = 1;
  select file as MASTER_READGAIN from calibFiles where
     (REFLEX.CATG=="MASTER_READGAIN") ;

  minRet = 0; maxRet = 1;
  select file as MASTER_2MASS_CATALOGUE_ASTROM from inputFiles where
     REFLEX.CATG =="MASTER_2MASS_CATALOGUE_ASTROM";
  minRet = 0; maxRet = 1;
  select file as MASTER_2MASS_CATALOGUE_PHOTOM from inputFiles where
     REFLEX.CATG =="MASTER_2MASS_CATALOGUE_PHOTOM";

  minRet = 0; maxRet = 1;
  select file as MASTER_PPMXL_CATALOGUE_ASTROM from inputFiles where
     REFLEX.CATG =="MASTER_PPMXL_CATALOGUE_ASTROM";
  minRet = 0; maxRet = 1;
  select file as MASTER_PPMXL_CATALOGUE_PHOTOM from inputFiles where
     REFLEX.CATG =="MASTER_PPMXL_CATALOGUE_PHOTOM";

  minRet = 0; maxRet = 1;
  select file as MASTER_LOCAL_CATALOGUE_ASTROM from inputFiles where
     REFLEX.CATG =="MASTER_LOCAL_CATALOGUE_ASTROM";
  minRet = 0; maxRet = 1;
  select file as MASTER_LOCAL_CATALOGUE_PHOTOM from inputFiles where
     REFLEX.CATG =="MASTER_LOCAL_CATALOGUE_PHOTOM";

  minRet = 1; maxRet = 1;
  select file as SCHLEGEL_MAP_NORTH from inputFiles where
     DO.CATG =="SCHLEGEL_MAP_NORTH";
  minRet = 1; maxRet = 1;
  select file as SCHLEGEL_MAP_SOUTH from inputFiles where
     DO.CATG =="SCHLEGEL_MAP_SOUTH";

  recipe hawki_science_process;

  product BASIC_CALIBRATED_SCI { PRO.CATG="BASIC_CALIBRATED_SCI";}
  product BASIC_VAR_MAP { PRO.CATG="BASIC_VAR_MAP";}  
  product BASIC_CALIBRATED_SKY { PRO.CATG="BASIC_CALIBRATED_SKY";}
  product BASIC_VAR_MAP_SKY { PRO.CATG="BASIC_VAR_MAP_SKY";}  
 
  product JITTERED_IMAGE_SCI { PRO.CATG="JITTERED_IMAGE_SCI";}
  product CONFIDENCE_MAP_JITTERED { PRO.CATG="CONFIDENCE_MAP_JITTERED";}
  product JITTERED_VAR_IMAGE { PRO.CATG="JITTERED_VAR_IMAGE";}

  product OBJECT_CATALOGUE_SCI {PRO.CATG="OBJECT_CATALOGUE_SCI";} 
  product OBJECT_CATALOGUE_JITTERED {PRO.CATG="OBJECT_CATALOGUE_JITTERED";} 

  product MEAN_SKY { PRO.CATG="MEAN_SKY";}
  product MEAN_SKY_VAR { PRO.CATG="MEAN_SKY_VAR";}

  product MATCHSTD_ASTROM { PRO.CATG="MATCHSTD_ASTROM";} // one created for each input frame
  product MATCHSTD_PHOTOM { PRO.CATG="MATCHSTD_PHOTOM";} // one created ONLY for the stack

}
    """

    soca_clean = "\n".join(
        (line + "//")[:(line + "//").index("//")] for line in soca.splitlines()
    )

    mylexer = OCALexer()
    for token in mylexer.tokenize(soca_clean):
        print(token)

    myparser = OCAParser()
    pprint(myparser.parse(mylexer.tokenize(soca_clean)))
