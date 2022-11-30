#!/usr/bin/env python

import Scientific.IO.NetCDF as nc
import numpy as np
from subprocess import call
import os

short_names = {
  301 : "ems_nox",
  302 : "ems_ch4",
  303 : "ems_co",
  304 : "ems_hcho",
  305 : "ems_c2h6",
  306 : "ems_c3h8",
  307 : "ems_me2co",
  308 : "ems_mecho",
  309 : "ems_c5h8",
  310 : "ems_bcff",
  311 : "ems_bcbc",
  312 : "ems_ocff",
  313 : "ems_ocbf",
  314 : "ems_monter",
  315 : "ems_nvoc",
  322 : "ems_bcbb",
  323 : "ems_ocbb",
  324 : "ems_so2bb",
  340 : "ems_noxair",
  34001 : "mmr_o3", 
  34002 : "mmr_no",
  34003 : "mmr_no3",
  34004 : "mmr_no2",
  34005 : "mmr_n2o5",
  34006 : "mmr_ho2no2",
  34007 : "mmr_hono2",
  34008 : "mmr_h2o2",
  34009 : "mmr_ch4",
  34010 : "mmr_co",
  34011 : "mmr_hcho",
  34012 : "mmr_meooh",
  34013 : "mmr_hono",
  34014 : "mmr_c2h6",
  34015 : "mmr_etooh",

}

long_names = {
  301 : "NOx surf emissions",
  302 : "CH4 surf emissions",
  303 : "CO surf emissions",
  304 : "HCHO surf emissions",
  305 : "C2H6 surf emissions",
  306 : "C3H8 surf emissions",
  307 : "Me2CO surf emissions",
  308 : "MeCHO surf emissions",
  309 : "C5H8 surf emissions",
  310 : "BC fossil fuel surf emissions",
  311 : "BC biofuel surf emissions",
  312 : "OC fossil fuel surf emissions",
  313 : "OC biofuel surf emissions",
  314 : "Monoterpene surf emissions",
  315 : "NVOC surf emissions",
  322 : "BC biomass 3D emission",
  323 : "OC biomass 3D emission",
  324 : "SO2 biomass burning emissions",
  340 : "NOx aircraft emissions",
  34001 : "O3 MASS MIXING RATIO AFTER TIMESTEP", 
  34002 : "NO MASS MIXING RATIO AFTER TIMESTEP",  
  34003 : "NO3 MASS MIXING RATIO AFTER TIMESTEP",  
  34004 : "NO2 MASS MIXING RATIO AFTER TIMESTEP",  
  34005 : "N2O5 MASS MIXING RATIO AFTER TSTEP",  
  34006 : "HO2NO2 MASS MIXING RATIO AFTER TSTEP",  
  34007 : "HONO2 MASS MIXING RATIO AFTER TSTEP",  
  34008 : "H2O2 MASS MIXING RATIO AFTER TSTEP",  
  34009 : "CH4 MASS MIXING RATIO AFTER TSTEP",  
  34010 : "CO MASS MIXING RATIO AFTER TSTEP",  
  34011 : "HCHO MASS MIXING RATIO AFTER TSTEP",
  34012 : "MeOOH MASS MIXING RATIO AFTER TSTEP",  
  34013 : "HONO MASS MIXING RATIO AFTER TSTEP",  
  34014 : "C2H6 MASS MIXING RATIO AFTER TSTEP",  
  34015 : "EtOOH MASS MIXING RATIO AFTER TSTEP",  
}

units = {
  301 : "kg.m-2.s-1",
  302 : "kg.m-2.s-1",
  303 : "kg.m-2.s-1",
  304 : "kg.m-2.s-1",
  305 : "kg.m-2.s-1",
  306 : "kg.m-2.s-1",
  307 : "kg.m-2.s-1",
  308 : "kg.m-2.s-1",
  309 : "kg.m-2.s-1",
  310 : "kg.m-2.s-1",
  311 : "kg.m-2.s-1",
  312 : "kg.m-2.s-1",
  313 : "kg.m-2.s-1",
  314 : "kg.m-2.s-1",
  315 : "kg.m-2.s-1",
  322 : "kg.m-2.s-1",
  323 : "kg.m-2.s-1",
  324 : "kg.m-2.s-1",
  340 : "kg.gridcell-1.s-1",
  34001 : "kg.kg-1", 
  34002 : "kg.kg-1",  
  34003 : "kg.kg-1",  
  34004 : "kg.kg-1",  
  34005 : "kg.kg-1",  
  34006 : "kg.kg-1",  
  34007 : "kg.kg-1",  
  34008 : "kg.kg-1",  
  34009 : "kg.kg-1",  
  34010 : "kg.kg-1",  
  34011 : "kg.kg-1", 
  34012 : "kg.kg-1",  
  34013 : "kg.kg-1",  
  34014 : "kg.kg-1",  
  34015 : "kg.kg-1",  

}

def get_list_of_varnames_to_change(file):

  returnList = [];

  # Get a list of variables
  variableNames = file.variables.keys()

  # Remove the dimensions from the variableNames
  dimensionNames = file.dimensions.keys()
  for d in dimensionNames:
    variableNames.remove(d)

  for vname in variableNames:
    var = file.variables[vname]
    attList = dir(var)
    if ( "long_name" in attList ):
      var_long_name = getattr( var, "long_name" )
      if ( var_long_name[:12] == "Stash code =" ):
        stash = int(var_long_name[12:])
        returnList.append({"old_name" : vname, "stash" : stash});

  return returnList

def main():
  filename = raw_input("Enter filename: ")

  # Open the file
  file = nc.NetCDFFile( filename, 'r' )

  varlist = get_list_of_varnames_to_change( file )

  file.close()

  for item in varlist:
    stash = item["stash"]
    old_name = item["old_name"]
    try:
      new_name = short_names[stash]
      new_long_name = long_names[stash]
      new_units = units[stash]
    except:
      print "Couldn't find the details for " + item["old_name"] + " (Stash code: " + str(stash) + ")"
      continue

    os.system('ncrename -h -O -v '+old_name+','+new_name+' '+filename)
    os.system('ncatted -O -h -a name,'+new_name+',o,c,'+new_name+' '+filename)
    os.system('ncatted -O -h -a long_name,'+new_name+',o,c,"'+new_long_name+'" '+filename)
    os.system('ncatted -O -h -a title,'+new_name+',o,c,"'+new_long_name+'" '+filename)
    os.system('ncatted -O -h -a stash_code,'+new_name+',o,i,'+str(stash)+' '+filename)
    os.system('ncatted -O -h -a units,'+new_name+',o,c,'+new_units+' '+filename)

if __name__ == "__main__":
  main()
