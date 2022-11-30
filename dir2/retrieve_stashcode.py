#!/apps/python/2.6/bin/python

import sys
import os
import Scientific.IO.NetCDF as nc
from operator import attrgetter

def main():

  try:
    filename = sys.argv[1]
    file = nc.NetCDFFile(filename, "r")
  except:
    print "Please enter filename as only parameter"
    raise

  dims = file.dimensions.keys()
  vars = file.variables.keys()

  varList = []

  # Remove all dimensions from the variable list
  for dimName in dims:
    vars.remove(dimName)

  # Add the details about all variables to the list.
  for varName in vars:
    v = file.variables[varName]
    varList.append(v)

  sList = sorted( varList, key=attrgetter('stash_section', 'stash_item') )

  for varItem in sList:
    print " {0:2d}, {1:3d}, {2}".format(  int(varItem.stash_section), \
                                        int(varItem.stash_item),    \
                                            varItem.long_name )
  print "Total: {0:d} entries".format(len(sList))
  
  file.close()


if __name__ == "__main__":
  main()
