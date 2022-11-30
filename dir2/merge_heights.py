#!/usr/bin/env python

import Scientific.IO.NetCDF as nc
import numpy as np
import os
import sys
sys.path.append("/home/599/hxw599/bin")
from change_varnames import get_list_of_varnames_to_change,units,short_names,long_names

def copy_atts( invar, outvar ):

  attribute_names = dir( invar )
  for obsolete_attribute in ['assignValue', 'getValue', 'typecode']:
    if obsolete_attribute in attribute_names:
      attribute_names.remove( obsolete_attribute )
  for attribute in attribute_names:
    setattr( outvar, attribute, getattr( invar, attribute ))


def main():

  output_height_name = 'hybrid_ht'

  infile_name = os.environ['INFILE']
  outfile_name = os.environ['OUTFILE']

  print infile_name + "    " + outfile_name

  infile = nc.NetCDFFile( infile_name, 'r' )
  outfile = nc.NetCDFFile( outfile_name, 'w' )

  for dimension in ['latitude', 'longitude', 't']:
    dim = infile.variables[dimension]
    if (dimension == 't'):
      dimsize = 0        # t is unlimited
    else:
      dimsize = dim.shape[0]
    outfile.createDimension( dimension, dimsize )
    outfile.createVariable( dimension, 'f', ( dimension, ) )
    outdim = outfile.variables[ dimension ]
    copy_atts( dim, outdim )
    outdim.assignValue(dim.getValue())

  # Heights:

  ht1 = infile.variables['hybrid_ht']
  try:
    ht2 = infile.variables['hybrid_ht_1']
  except:
    print "ht2 not found"
    ht2 = np.array([]);

  total_number_of_levels = ht1.shape[0] + ht2.shape[0]

  outfile.createDimension( output_height_name, total_number_of_levels )
  outfile.createVariable( output_height_name, 'f', ( output_height_name, ) )

  if (ht1.shape[0] == 1) :
    height = ht1.getValue()
    height.resize( total_number_of_levels )
    height[1:] = ht2.getValue()
  else :
    height = [ht2.getValue()]
    height.resize( total_number_of_levels )
    height[1:] = ht1.getValue()

  outheight = outfile.variables[output_height_name]
  copy_atts( ht1, outheight )
  setattr( outheight, 'units', 'm' )
  outheight.assignValue( height )

  varname_to_stash = get_list_of_varnames_to_change( infile )

  stash_to_varname = {}
  for item in varname_to_stash:
    stash = item['stash']
    if not stash in stash_to_varname:
      stash_to_varname[stash] = [item['old_name']]
    else:
      stash_to_varname[stash].append(item['old_name'])

  for stash in stash_to_varname:
    list_of_vars = stash_to_varname[stash]
    name = short_names[stash]
    title = long_names[stash]
    outfile.createVariable( name, 'f', ( 't', output_height_name, 'latitude', 'longitude', ) )
    outvar = outfile.variables[name]
    values = outvar.getValue() 
    print values.shape
    for invar_name in list_of_vars:
      invar = infile.variables[ invar_name ]
      copy_atts( invar, outvar )
      indata = invar.getValue()
      print indata.shape
      if indata.shape[1] == 1:
        print "Set field " + invar_name + " as bottom layer for " + name
        values[:,0,:,:] = indata[ :, 0, :, : ]
      else :
        print "Set field " + invar_name + " as other layers for " + name
        values[:,1:,:,:] = indata

    setattr( outvar, 'long_name', title )
    setattr( outvar, 'title', title )
    setattr( outvar, 'name', name )
    setattr( outvar, 'units', units[stash] )
    setattr( outvar, 'stash_code', stash )

    outvar.assignValue( values )

  infile.close()
  outfile.close()

if __name__ == "__main__":
  main()
  
