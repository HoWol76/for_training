#!/usr/bin/env python

# A python script to read a STASHC file and write the fields in a more
# human-readable format. The variables are written using stash codes, 
# long names, and the time and domain profiles, similar to the format
# used in the UM stash panel. This makes reading the STASHC files used
# for coupled models somewhat easier.
# 
# Also, the variables are sorted by the stash codes, if already not so. 
# This facilitates the comparison between two STASHC files.
#
# The coupling fields are excluded from processing, because of ambiguity
# in the definitions of TIME and DOMAIN profiles (also, these fields
# will likely remain unchanged).
#
# You need to have stashvar.py in your pythonpath to run this script.
#
# 22-SEP-2011  Harun Rashid
#

import sys, os, operator
import re, socket
#from stashvar import atm_stashvar as atm  # see below

if  len(sys.argv) < 2:
   print "Usage:"
   print "  "+os.path.basename(sys.argv[0])+"   STASHC"
   sys.exit(1)

stfil = sys.argv[1]

hostname = os.environ.get("PBS_O_HOST")
if not hostname:
    hostname=socket.gethostname() 

try:
    from stashvar import atm_stashvar as atm
except:
    if re.match('vayu\d*',hostname):
       sys.path.append('/home/559/hxw599/app/trunk/database')
    elif re.match('cherax*',hostname):
       sys.path.append('/cs/home/csdar/wol052/app/trunk/database')
    else:
       print "Unknown machine! Can't import stashvar module."
       sys.exit(2)
    from stashvar import atm_stashvar as atm

#stfil = "hg2-r1.1-M2_PiCntrl/STASHC_GregMonMean2"
#stfil = "hg2-r1.1-M2_PiCntrl/STASHC_cmip5_MonDai2"

f = open(stfil)
st1 = f.readlines()
f.close()

dic1 = {}
sttim = []
stdom = []
stuse = []
stash_list = []
stash_dict = {}
lines = []
i=0
j=0
for ln in st1:
  if ln.strip().startswith("&STREQ"):
     isec = int(ln.split(",")[1][6:])
     item = int(ln.split(",")[2][6:])
     stash = 1000*isec+item
     stash_list.append(stash)
     stash_dict[i] = stash
     lines.append(ln)
     #dic1[stash] = ln
     i = i+1
  elif ln.strip().startswith("&TIME"):
     sttim.append(ln)
  elif ln.strip().startswith("&DOMAIN"):
     stdom.append(ln)
  elif ln.strip().startswith("&USE"):
     stuse.append(ln)
  elif ln.strip().startswith("&STASHNUM"):
     if j > 0: break                # don't process the coupling fields
     j = j+1

# sort stash_dict by value (operator.itemgetter(1)). Sorting based on a
# dictionary (such as "dic1" above) eliminates the multiple occurrences 
# of stash codes.

stash_sorted = sorted(stash_dict.iteritems(), key=operator.itemgetter(1))

# Now sort "lines" according to stash code (this retains the multiple 
# occurrences of stash codes).
 
lines_sorted = []
i = 0
for ln in lines:
  k = stash_sorted[i][0]
  lines_sorted.append(lines[k])
  i = i+1

# Get the time profiles
time_prof = {}
for i in range(len(sttim)):
  time_prof[i+1] = sttim[i].split('"')[1]

# Get the domain profiles
dom_prof = {}
for i in range(len(stdom)):
  dom_prof[i+1] = stdom[i].split('"')[1]

# Get the use profiles
use_prof = {}
for i in range(len(stuse)):
  use_prof[i+1] = stuse[i].split('"')[1]

stfld = []
for ln in lines_sorted:
   isec = ln.split(",")[1][6:]
   item = ln.split(",")[2][6:]
   idom = int(ln.split(",")[3][6:])
   itim = int(ln.split(",")[4][6:])
   iuse = int(ln.split(",")[5][6:8])
   k = 1000*int(isec)+int(item)
   try:
      long_name = atm[k][0]
   except:
      long_name = "*******"
   #stf = "ISEC="+isec+", ITEM="+item+", ["+long_name+"]"+\
   #          ", ITIM="+time_prof[itim]+", IDOM="+dom_prof[idom]+" \n"
   stf = "ISEC=%2s, ITEM=%3s,  [%-35s], ITIM=%-6s, IDOM=%-4s, IUSE=%-4s \n" \
         % (isec,item,long_name,time_prof[itim],dom_prof[idom],use_prof[iuse])
   stfld.append(stf)


fo = open(os.path.basename(stfil)+"_sorted","w")
fo.writelines(lines_sorted)
fo.close()

fo = open(os.path.basename(stfil)+"_transl","w")
fo.writelines(stfld)
fo.close()




