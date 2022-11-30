#!/apps/python/2.6/bin/python
#
# A python script to convert the CMIP5 fields (atmospheric) from
# UM fieldsfiles to netcdf format. This script works for all the
# four types of fields (monthly, daily, 6-hourly, and 3-hourly).
# For min, max fields, also need to match on cell_methods attribute
# Assume these are "time0: min" and "time0: max".
#
# The input variable names are mapped to CMIP5 variable names before 
# writing to netcdf files. Also, singleton dimensions are eliminated,
# coordinate names are mapped to the commonly used names, and the time
# dimension is written as 'unlimited'. This is helpful for creating 
# timeseries for one or more variables and writing them to a netcdf
# file, e.g.:
#     ncrcat -h -v tas multiple_input_files.nc single_output_file.nc
# 
# Climate diagnostics on pressure levels are normally masked;
# nomask option turns this off (special case for runs where the
# heavyside function, used for masking, were not saved).
#
# Note:
#   Python version 2.6 needs to be used at the moment, because
# of compatibility issue with the "Nio" module (see below). Also,
# this script uses Petteri's installation of cdat-lite and PyNio 
# at this stage. This will be changed to a common, system-wide 
# installation later.
#
# Acknowledgement:
#   This script is designed taking ideas from previous python scripts
# written by Martin Dix and Petteri Uotila.
#
# Harun Rashid (harun.rashid@csiro.au)
# 20-JUL-2011
#

import os, sys, getopt
import numpy as np
import re
from datetime import datetime
import socket

ifile = None
ofile = None
mask = True
heavyside = False

def usage():
    print " "
    print "Usage:"
    print "   "+os.path.basename(sys.argv[0]) + " -i ifile -o ofile [--nomask]"
    message = """
     arguments:  
       ifile =>> input UM filename 
       ofile =>> output netCDF filename
       nomask =>> don't mask the pressure-level variables
                  with the heavyside function (psag)
                  [default: masking is done (recommended), 
                   if psag is in the UM input file.]
    """
    print message
    return

# Process the command-line inputs
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:',['nomask'])
except getopt.GetoptError, err:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':
        ifile = a
    elif o == '--nomask':
        mask = False
    elif o == '-o':
        ofile = a

if not ifile or not ofile:
   usage()
   sys.exit(2)

print "Using python version: "+sys.version.split()[0]

hostname = os.environ.get("PBS_O_HOST")
if not hostname:
    hostname=socket.gethostname() 

if re.match('vayu\d*',hostname):
    #pythonhome='/home/565/pju565'
    pju_home = '/home/565/pju565'
    sys.path.append(os.path.join(pju_home,'lib','python2.6',\
                'site-packages','cdat_lite-5.2_1-py2.6-linux-x86_64.egg'))
elif re.match('solar\d*',hostname):
    #pythonhome='/g/sc/ophome/nmoc_share/local/gcc_builds/Python-2.6.4'
    sys.path.append('/g/sc/home/cawcr_share/cdat52/lib/python2.5/site-packages/')
    pythonhome='/g/sc/home/uot001/'
elif re.match('cherax*',hostname):
    #pythonhome='/g/sc/ophome/nmoc_share/local/gcc_builds/Python-2.6.4'
    sys.path.append('/cs/home/csdar/uot001/lib/python')
    sys.path.append('/tools/cdat/5.0.0/lib/python2.5/site-packages')
    pythonhome='/tools/cdat/5.0.0/bin/'
else:
    pythonhome='/home/565/pju565'
    if not os.path.exists(pythonhome):
        pythonhome=os.getenv('HOME')
    sys.path.append(os.path.join(pythonhome,'lib','python2.6','site-packages',\
                                 'cdat_lite-5.2_1-py2.6-linux-x86_64.egg'))

sys.path.append(os.path.join(pju_home,'lib','python2.6','site-packages','PyNIO'))
try:
    import stashvar
    print "imported default stashvar"
except:
    if re.match('vayu\d*',hostname):
       sys.path.append('/home/599/hxw599/app/trunk/database')
    elif re.match('cherax*',hostname):
       sys.path.append('/cs/home/csdar/wol052/app/trunk/database')
    else:
       print "Unknown machine! Can't import stashvar module."
       sys.exit(2)
    import stashvar
    print "imported svn stashvar"

import cdms2, cdtime
from cdms2 import MV
import Nio

# Rename dimension to commonly used names
renameDims = {'latitude0':'lat','longitude0':'lon','latitude1':'lat_1',\
              'longitude1':'lon_1','z4_p_level':'lev','z9_p_level':'lev',\
              'z3_p_level':'lev','time0':'time','time1':'time_1'}

# Exclude the singleton dimensions from the output neCDF file
excludeDims = ['z0_surface','z10_msl','z3_toa','z4_level','z7_height',\
               'z1_level','z2_height','z5_msl','z8_level','z2_msl',\
               'z4_surface','z2_level','z3_height','z4_soil']

# a function to create dimensions in the netCDF file
def write_nc_dimension(dimension,fi,fo):
    dobj = fi.dimensionobject(dimension)
    dval = dobj.getData()
    # make the time dimension "unlimited"
    if dobj.id == 'time0':
        dimlen = None
    else:
        dimlen = len(dval)
    # see if we need to rename output netcdf dimension name
    try:
        dimout = renameDims[dimension] if dimension in renameDims else dimension
        if dimout not in fo.variables.keys():
            fo.create_dimension(dimout,dimlen)
            if hasattr(dobj,'standard_name') and dobj.standard_name == 'time':
                fo.create_variable(dimout,'d',(dimout,))
            else:
                fo.create_variable(dimout,dval.dtype.char,(dimout,))
            for dattr in dobj.attributes:
                setattr(fo.variables[dimout],dattr,getattr(dobj,dattr))
            fo.variables[dimout][:] = dval
    except:
        dimout = dimension
        if dimout not in fo.variables.keys():
           fo.create_dimension(dimension,dimlen)
           if hasattr(dobj,'standard_name') and dobj.standard_name == 'time':
               fo.create_variable(dimension,'d',(dimension,))
           else:
               fo.create_variable(dimension,dval.dtype.char,(dimension,))
           for dattr in dobj.attributes:
               setattr(fo.variables[dimension],dattr,getattr(dobj,dattr))
           fo.variables[dimension][:] = dval
    # update dimension mapping
    if dimension in renameDims:
        renameDims[dimension] = dimout
    print "Wrote dimension %s as %s." % (dimension,dimout)


# Main program begins here. 
# First, open the input UM file (fieldsfile)  

try:
    fi = cdms2.open(ifile)
except:
    print "Error opening file", ifile
    sys.exit(1)

if os.path.exists(ofile):
    os.unlink(ofile)

# Create an output netCDF file
fo = Nio.open_file(ofile,'w')
history = "Converted to NetCDF by %s on %s." % (os.getenv('USER'),datetime.now().strftime("%Y-%m-%d"))

# global attributes
for attribute in fi.attributes:
    if attribute in ['history']:
        setattr(fo,attribute,"%s. %s" % (getattr(fi,attribute),history))
    else:
        setattr(fo,attribute,getattr(fi,attribute))

# variables to write
varnames = fi.listvariables()

# collect list of dimensions associated with these variables
dims = set(fi.listdimension())             # set of all dim_names in the file
dimns = list(dims.difference(excludeDims)) # exclude those in excludeDims
dimns.sort()

# create dimensions
for dimension in dimns:
    write_nc_dimension(dimension,fi,fo)
print "Finished writing dimensions..."; sys.stdout.flush()

umvar_atts = ["name","long_name","standard_name","units"]
hcrit = 0.5               # critical value of Heavyside function for inclusion.

# loop over all variables
for varname in varnames:
    vval = fi.variables[varname]
    sp = vval.shape
    if len(sp) == 4 and sp[1] == 1:
       vval = vval[:,0,:,:]                # remove the singleton vertical dim
    vdims = vval.listdimnames()
    # see if we need to rename variables netcdf dimensions
    for vdidx, vdim in enumerate(vdims):
        if vdim in renameDims:
            vdims[vdidx] = renameDims[vdim]
    if hasattr(vval,'stash_item') and hasattr(vval,'stash_section'):
        stash_section = vval.stash_section[0]
        stash_item = vval.stash_item[0]
        item_code = vval.stash_section[0]*1000 + vval.stash_item[0]
        umvar = stashvar.StashVar(item_code,vval.stash_model[0])
        vname = umvar.name

        if hasattr(vval,"cell_methods") and vval.cell_methods == "time0: max":
            vname = vname+"max"
        if hasattr(vval,"cell_methods") and vval.cell_methods == "time0: min":
            vname = vname+"min"

        if (30201 <= item_code <= 30303) and mask:
            # P LEV/UV GRID with missing values treated as zero;
            # needs to be corrected by Heavyside fn
            if not heavyside:
                heavyside = fi.variables['psag']
                # check variable code as well as the name.
                if heavyside.stash_item[0] != 301 or \
                                            heavyside.stash_section[0] != 30:
                    raise error, "Heavyside variable code mismatch"
            fVal = vval.getMissing() 
            if vval.shape == heavyside.shape:
                vval = MV.where(np.greater(heavyside,hcrit),vval/heavyside,fVal)
                vval.fill_value = vval.missing_value = fVal
            else:
                print vname,vval.shape,'!= heavyside',heavyside.shape
                print vname+' not masked'

        # write data
        #fo.create_variable(vname,vval.dtype.char,tuple(vdims))
        try:
            fo.create_variable(vname,vval.dtype.char,tuple(vdims))
            fo.variables[vname][:] = vval
            print "%15s written..." % vname; sys.stdout.flush()
        except:
            print "Could not write %s!" % vname
            vname = vname+'_1'
            fo.create_variable(vname,vval.dtype.char,tuple(vdims))
            fo.variables[vname][:] = vval
            print "Now written as %15s ..." % vname; sys.stdout.flush()


        # variable attributes
        for vattr in vval.listattributes():
            if getattr(vval,vattr) is None:
                print "Could not write attribute %s for %s." % (vattr,vname)
            else:
                setattr(fo.variables[vname],vattr,getattr(vval,vattr))
        for vattr in umvar_atts:
            if hasattr(umvar,vattr) and getattr(umvar,vattr) != '':
                setattr(fo.variables[vname],vattr,getattr(umvar,vattr)) 

        #print "%15s written..." % vname; sys.stdout.flush()

fo.close() 
fi.close()




