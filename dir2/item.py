#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import sys

ListOfElements = [
   "Model", "Section", "Item", "Description", 
   "Space", "Point", "Time", "Grid", "LevelT", "LevelF", "LevelL", "PseudoT", "PseudoF", "PseudoL", "LevCom", 
   "OptionCodes", "VersionMask", "Halo", 
   "DataT", "DumpP", "PC", 
   "Rotate", "PPFC", "LBVC"
   # "User", "BLEV", "TLEV", "RBLevV", "CFLL", "CFFF" are no longer used
   ]
ListOfAsYetUnwrittenElements = ["VersionMask", "DumpP", "PPFC", "LBVC"]

ModelSelector = {
   1:    "Atmosphere",
   2:    "Ocean (depreciated)", 
   3:    "Slab Ocean (depreciated)",
   4:    "Wave (depreciated)"
   }

SpaceSelector = {
   0:    "Diagnostic field for which space is required only when the diagnostic is requested", 
   1:    "Non-prognostic field for which space is always required", 
   2:    "Section 0, 33, 34 only: primary field available to STASH", 
   3:    "Section 0, 33, 34 only: primary field unavailable to STASH which is addressed in the dump and D1", 
   4:    "Section 0 only: primary field which is addressed in D1 only (Pre-UM 5.0)", 
   5:    "Section 0 only: primary field which is addressed in the dump only (Pre-UM 5.0)", 
   6:    "Diagnostic field for which space is required when requested or implied by other diagnostics", 
   7:    "Non-primary field which points back to a section 0 field", 
   8:    "Dual time ocean prognostic. (Pre-UM 7.0)", 
   9:    "Extra items at the end of D1 for internal fields", 
   10:   "Field not held in D1 or the dump, including LBC out fields"
   }

TimeSelector = {
   1:    "Every time step",
   2:    "Every long wave radiation time step",
   3:    "Every short wave radiation time step", 
   4:    "Every coupling period", 
   5:    "Every call of atmospheric climate meaning period 1", 
   6:    "Every call of atmospheric climate meaning period 2", 
   7:    "Every call of atmospheric climate meaning period 3", 
   8:    "Every call of atmospheric climate meaning period 4", 
   13:   "Every convection time step", 
   14:   "Every leaf phenology time step", 
   15:   "Every vegetation timestep", 
   16:   "Every river routing timestep"
   }

GridSelector = {
   1:    "Data on atmospheric theta points", 
   2:    "Data on atmospheric theta points. land only", 
   3:    "Data on atmospheric theta points. sea only", 
   4:    "Data on atmospheric zonal theta points", 
   5:    "Data on atmospheric meridional theta points", 
   11:   "Data on atmospheric uv points", 
   12:   "Data on atmospheric uv points, land only", 
   13:   "Data on atmospheric uv points, sea only", 
   14:   "Data on atmospheric uv zonal points", 
   15:   "Data on atmospheric meridional uv points", 
   17:   "Atmospheric Scalar", 
   18:   "Data on atmospheric u points on the ?????", 
   19:   "Data on atmospheric v points on the ?????", 
   21:   "Data compressed to atmospheric land points", 
   22:   "Data on the ozone grid", 
   23:   "Data on the river routing grid (UM5.5 and later)", 
   25:   "Data on the atmospheric LBC grid (pre-UM5.0)", 
   26:   "Lateral boundary data at atmospheric theta points", 
   27:   "Lateral boundary data at atmospheric u points", 
   28:   "Lateral boundary data at atmospheric v points", 
   29:   "Orography field for atmospheric LBCs"
   }

LevelTSelector = {
   0  :  "Unspecified level", 
   1  :  "Data on atmospheric rho levels / full model levels (pre-UM5.0) / ocean levels (pre-UM7.0)", 
   2  :  "Data on atmospheric theta levels / half (?)", 
   3  :  "Data on pressure levels", 
   4  :  "Data on geometric height levels (pre-UM5.0)", 
   5  :  "Single level data", 
   6  :  "Data on deep soil levels", 
   7  :  "Data on theta levels", 
   8  :  "Data on potential vorticy levels (ascending order) (pre-UM5.0)", 
   9  :  "Data on cloud threshold levels (octas) (pre-UM5.0)", 
   11 :  "Data on ISCCP levels (from UM5.5)"
   }

LevelFLSelector = {
   -1 :  "Unset, this must be used for single level data", 
   1  :  "First atmospheric level", 
   2  :  "Top atmospheric level", 
   3  :  "Top wet level", 
   4  :  "Top atmospheric level -1", 
   5  :  "First level in boundary layer", 
   6  :  "Last level in boundary layer", 
   7  :  "First level above boundary layer", 
   8  :  "First soil level", 
   9  :  "Last soil level", 
   10 :  "First tracer level (allowed to be >1)", 
   11 :  "Last tracer level (= Top atmospheric level)", 
   12 :  "Last gravity wave drag level +1", 
   13 :  "First gravity wave drag level", 
   14 :  "Last gravity wave drag level", 
   15 :  "Fist level in vertical diffusion routine", 
   16 :  "Last level in vertical diffusion routine -1", 
   17 :  "Last level in vertical diffusion routine", 
   18 :  "Last level in boundary layer -1", 
   19 :  "Top level of atmosphere +1", 
   20 :  "First soil level +1", 
   21 :  "First ocean level (top) (pre-UM7.0)", 
   22 :  "Last ocean level (bottom) (pre-UM7.0)", 
   23 :  "Top ozone level", 
   24 :  "Number of atmospheric levels * SW bands", 
   25 :  "(Number of atmospheric levels +1) * SW bands", 
   26 :  "Number of wet levels * SW bands", 
   27 :  "Number of atmospheric levels * LW bands", 
   28 :  "(Number of atmospheric levels +1) * LW bands", 
   29 :  "Number of wet levels * LW bands", 
   32 :  "Number of SW radiation bands", 
   33 :  "Number of LW radiation bands", 
   34 :  "Number of soil hydrology levels", 
   35 :  "Number of cloudy levels", 
   38 :  "Zeroth atmospheric level (from UM5.0)", 
   39 :  "Number of ISCCP levels (from UM5.5)"
   }

PseudoTSelector = {
   0  :  "None", 
   1  :  "Short Wave radiation bands", 
   2  :  "Long Wave radiation bands", 
   3  :  "Atmospheric assimilation group", 
   8  :  "HadCM2 Sulphate Loading Pattern Index", 
   9  :  "Land and Vegetation Surface types", 
   10 :  "Multiple-Category sea-ice (from UM5.5)", 
   11 :  "Aerosol modes (from UM7.1)", 
   12 :  "Aerosol emission classes (reserved, but not yet implemented)"
   }

PseudoFSelector = {
   0  :  "Disabled", 
   1  :  "Dimension starts at 1", 
   21 :  "Dimension starts at the first group for the atmospheric assimilation set 'P* observation'", 
   22 :  "Dimension starts at the first group for the atmospheric assimilation set 'Theta observation'", 
   23 :  "Dimension starts at the first group for the atmospheric assimilation set 'U, V observation'", 
   24 :  "Dimension starts at the first group for the atmospheric assimilation set 'Relative Humidity observation'", 
   25 :  "Dimension starts at the first group for the atmospheric assimilation set 'Rainfall rate observation'"
   }

PseudoLSelector = {
   0  :  "Disabled", 
   1  :  "Number of short wave bands", 
   2  :  "Number of long wave bands", 
   3  :  "(Number of mead types) * (Number of ocean basins)", 
   6  :  "Number of sulphate loading patterns", 
   7  :  "Total number of surface types", 
   8  :  "Number of surface types that are vegetation", 
   9  :  "Number of land surface tiles (from UM5.2)", 
   10 :  "Number of sea-ice categories (from UM5.5)", 
   21 :  "Last group for the atmospheric assimilation set 'P* observation'", 
   22 :  "Last group for the atmospheric assimilation set 'Theta observation'", 
   23 :  "Last group for the atmospheric assimilation set 'U, V observation'", 
   24 :  "Last group for the atmospheric assimilation set 'Relative Humidity observation'", 
   25 :  "Last group for the atmospheric assimilation set 'Rainfall rate observation'"
   }

LevComSelector = {
   0  :  "STASH receives input on all available levels and pseudo-levels", 
   1  :  "STASH receives the diagnostic input on the STASH input levels"
   }

HaloSelector = {
   1  :  "Single point halo", 
   2  :  "Extended halo", 
   3  :  "No halo"
   }

DataTSelector = {
   1  :  "Real", 
   2  :  "Integer", 
   3  :  "Logical"
   }

RotateSelector = {
   0  :  "Data is either non-vectorial or is relative to the model",
   1  :  "Data is passed to the STASH relative to the lat/long grid"
   }



# Stash Option Lists:

stashOptionNames = {
   # Key: SectionForLookUp * 100 + n-Number
   #                                SECTION 0, 31, 32, 33, 34 : 
   # SectionForLookUp = 0
   3     :  "Hydrology",
   4     :  "Aerosol",
   5     :  "Orog.Rough.",
   6     :  "Interface",
   7     :  "Coupling",
   8     :  "Extra",
   9     :  "Orog. Grad.",
   10    :  "Sulphur",
   11    :  "Vegetation",
   12    :  "M. Phase",
   13    :  "2D/3D Cloud",
   14    :  "Soot",
   15    :  "RHcrit",      # not used currently
   16    :  "Carb. Cycle",
   17    :  "Var reconf",  # as in all sections
   18    :  "Coastal",
   19    :  "Tropopause",
   20    :  "Therm.Vege.",
   21    :  "Biom. Aero.",
   22    :  "Riv-routing",
   23    :  "Mul sea-ice",
   24    :  "Miner. Dust",
   25    :  "STOCHEM 1",
   26    :  "STOCHEM 2",
   27    :  "CCRad",
   28    :  "Cariolle O3",
   29    :  "FFOC aero",
   #                                SECTION 1: Short wave radiation
   101   :  "Gl. Model",
   102   :  "Cloud Phy",
   103   :  "HadCM2 rad",
   104   :  "Indir. SA",
   105   :  "Sea-salt",
   106   :  "PC2",
   #                                SECTION 2: Long wave radiation
   201   :  "Match O3",
   206   :  "PC2",
   #                                SECTION 3: Boundary Layer
   301   :  "Orog.Rough.",
   302   :  "SO2/NH3/Soo",
   303   :  "Carb. cycle",
   304   :  "Mul Sea-ice",
   306   :  "PC2",
   }

stashOptionList = {
   # SectionForLookUp*1000 + n-number * 10 + item number
   # ----------------------------------------------------------------------------------
   #                                SECTIONS 0, 31, 32, 33, 34
   # Hydrology indicator
   31    :  "Item included for single-layer hydrology (pre-UM4.5)",
   32    :  "Item included for multi-layer hydrology (pre-UM4.5)",
   33    :  "Item included only for MOSES hydrology",
   34    :  "Item excluded from single-layer hydrology",
   35    :  "Item included for large scale (TOPMODEL) hydrology scheme",
   # Aerosol climatology indicator
   41    :  "Item included only for biogenic aerosol climatology (stash code 351)",
   42    :  "Item included only for biomass burning aerosol climatology (stash code 352, 353, 354)",
   43    :  "Item included only for black carbon aerosol climatology (stash codes 355, 356)",
   44    :  "Item included only for sea salt aerosol climatology (stash codes 357, 368)",
   45    :  "Item included only for sulphate aerosol climatology (stash codes 359, 360, 361)",
   46    :  "Item included only for dust aerosol climatology (stash codes 362-367)",
   47    :  "Item included only for organic carbon aerosol climatology (stash codes 368, 369, 370)",
   48    :  "Item included only for delta aerosol climatology (stash code 371)",
   # Orographic roughness indicator
   51    :  "Item excluded when orographic roughness used",
   52    :  "Item included only when orographic roughness used",
   # Interface indicator
   61    :  "Item included only in limited area models",
   62    :  "Item included only for models with lower boundary",
   # Coupling indicator
   71    :  "Item included only if OASIS coupling is used",
   72    :  "Item currently unconditionally excluded",
   77    :  "Coupled run with DMS ocean flux (UM6.2-UM6.6)",
   # Extra fields indicator
   81    :  "Item included only for SST anomaly runs",
   84    :  "Item included only for total aerosol runs",
   85    :  "Item included only for total aerosol emission runs",
   86    :  "Item included only if snow albedo scheme used",
   88    :  "Item included only if Energy Adjustment Scheme (section 14) used",
   # Orographic Gradient component indicator
   91    :  "Item included only if orographic gradient used",
   92    :  "Item included only if gradient correction for short wave radiation used",
   # Sulphur Cycle indicator
   101   :  "Item included only for SO2 sulphur cycle",
   102   :  "Item included only for SO2 with surface emissions",
   103   :  "Item included only for SO2 with high level emissions",
   104   :  "Item included only for SO2 with natural emissions",
   105   :  "Item included only for SO2 with DMS cycle",
   106   :  "Item included only for SO2 with DMS cycle and emissions",
   107   :  "Item included for SO2 with O3 oxidation included",
   108   :  "Item included for SO2 with O3 oxidation and NH3 included",
   109   :  "Item included only for SO2 with O3 oxidation and NH3 emissions",
   # Vegetation parametrization indicator
   111   :  "Item included only if direct vegetation parametrization not used",
   112   :  "Item included only for direct vegetation parametrization with or without competition",
   113   :  "Item included only for direct vegetation parametrization with competition",
   # Mixed phase precipitation
   121   :  "Item included in secondary space if Mixed phase precipitation is not used",
   122   :  "Item included as prognostic if Mixed phase precipitation scheme is used",
   123   :  "Item included if Mixed phase precip and prognostic cloud ice (crystals) used",
   124   :  "Item included if Mixed phase precip and prognostic rain used",
   125   :  "Item included if Mixed phase precip and prognostic graupel used",
   126   :  "Item included if PC2 scheme is used (from UM6.0)",
   # 2D or 3D convective cloud amount indicator
   131   :  "Item included only if CCA is 2D (anvil code OFF)",
   132   :  "Item included only if CCA is 3D (anvil code ON)",
   # Soot scheme indicator
   141   :  "Item included for soot scheme only",
   142   :  "Item included for soot scheme with surface emissions",
   143   :  "Item included for soot scheme with high level emissions",
   # RHcrit would be n15, but is not used
   # Carbon cycle indicator
   161   :  "Item included only for carbon cycle",
   # Var reconfiguration indicator
   171   :  "Item included for VAR reconfiguration",
   # Coastal tiling indicator
   181   :  "Item included only if coastal tiling is used",
   # Tropopause bazed ozone indicator (from UM5.3)
   191   :  "Item included only if tropopause based ozone is used (from UM5.3)",
   # Thermal vegetation canopy
   201   :  "Item included for snow canopy only",
   # Biomass aerosol scheme indicator
   211   :  "Included if biomass modelling is used",
   212   :  "Included if surface emissions used",
   213   :  "Included if elevated emissions used",
   # River-routing indicator
   221   :  "Included if river-routing scheme is used",
   222   :  "Included if inland basin flow scheme is used (from UM6.2)",
   # Multiple sea-ice categories indicator
   231   :  "Included if multiple sea-ice categories selected",
   # Mineral dust scheme indicator
   241   :  "Included if mineral dust scheme used",
   # STOCHEM scheme indicator 1 (from UM6.1)
   251   :  "Included if STOCHEM methane (CH4) is used",
   252   :  "Included if STOCHEM ozone (O3) is used",
   # STOCHEM scheme indicator 2 (from UM6.2)
   261   :  "Included if PAR (photochemically active radiation) is used",
   # CCRad scheme indicator
   271   :  "Item included if CCRad scheme used (from UM6.6)",
   272   :  "Item included if CCRad scheme and 3d_CCW is used (from UM6.6)",
   # Cariolle ozone tracer scheme
   281   :  "Included if Cariolle ozone transport and basic chemistry used",
   # Fossil-fuel organic carbon (FFOC) aerosol scheme indicator
   291   :  "Included if fossil-fuel organic carbon (FFOC) modelling used (from UM7.1)",
   292   :  "Included if fossil-fuel organic carbon (FFOC) surface emissions used (from UM7.1)",
   293   :  "Included if fossil-fuel organic carbon (FFOC) elevated emissions used (from UM7.1)",
   # -------------------------------------------------------------------------------------
   #                                               SECTION 1: Short Wave Radiation
   # Global model indicator
   1011  :  "Item available only for global atmoshere",
   # Cloud microphysics indicator
   1021  :  "Item available only if cloud microphysics used",
   # HadCM2 approximate radiatve effects of sulphate indicator
   1031  :  "Item available only if HadCM2 approximate radiative effects of sulphate used",
   # Indirect effect fo sulphate aerosol (SA) in SW radiation
   1041  :  "Item available only if indirect effect of sulphate aerosol in SW radiation requested",
   # Effect of sea salt parametrization in SW radiation
   1051  :  "Item available only if direct or indirect effects of sea-salt in SW radiation",
   # PC2 cloud scheme indicator
   1061  :  "Item available only if PC2 cloud scheme is used",
   # -------------------------------------------------------------------------------------
   #                                               SECTION 2: Long Wave Radiation
   # Matching of ozone tropopause
   2011  :  "Item is available if matching of ozone tropopause selected",
   # PC2 cloud scheme indicator
   2061  :  "Item available only if PC2 cloud scheme is used",
   # -------------------------------------------------------------------------------------
   #                                               SECTION 3: Boundary Layer
   # Orographic Roughness indicator
   3011  :  "Item is available only if orographic roughness is used",
   # SO2 sulphur cycle / NH3 / Soot indicator
   3021  :  "Item available only if SO2 sulphur cycle is used",
   3022  :  "Item available only if NH3 scheme is used",
   3023  :  "Item available only if soot scheme is used",
   3024  :  "Item available if biomass scheme is used",
   3025  :  "Item available if mineral dust scheme is used",
   3026  :  "Item available if fossil-fuel organic carbon (FFOC) scheme is used",
   # Carbon cycle indicator
   3031  :  "Item included only if carbon cycle is used",
   # Multiple sea-ice categories indicator
   3041  :  "Available if multiple sea-ice categories selected",
   # PC2 cloud scheme indicator
   3061  :  "Item available only if PC2 cloud scheme is used",
   
   }

def newStashItem():
   # Creates an empty stashItem dictionary with all relevant entries at least present.
   stashItem = {
      "Model"        : 0,
      "Section"      : 0,
      "Item"         : 0,
      "Description"  : "",
      "Space"        : 0,
      "Point"        : 0, 
      "Time"         : 0,
      "Grid"         : 0,
      "LevelT"       : 0,
      "LevelF"       : 0,
      "LevelL"       : 0,
      "PseudoT"      : 0,
      "PseudoF"      : 0,
      "PseudoL"      : 0,
      "LevCom"       : 0,
      "OptionCodes"  : "000000000000000000000000000000",
      "VersionMask"  : "00000000000000000000",
      "Halo"         : 0,
      "DataT"        : 0,
      "DumpP"        : 0,
      "PC"           : [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99],
      "Rotate"       : 0,
      "PPFC"         : 0,
      "User"         : 0,
      "LBVC"         : 0,
      "BLEV"         : 0,
      "TLEV"         : 0,
      "RBLevV"       : 0,
      "CFLL"         : 0,
      "CFFF"         : 0
      }
   return stashItem

def analyseOptions(stashItem):
   # -----------------------------------------------
   # Analyses the 'OptionCodes' entry in the STASHmaster
   # file.
   # The meaning of the options might change according to 
   # The section of the item.
   numOptions = len(stashItem["OptionCodes"])
   options = {}

   # Generate an array of the OptionCodes. Note that the 
   # Option codes are reversed:
   # OpionCodes = n30n29n28...n2n1
   n = [0]                          # In the documentation, the options start with index 1,
                                    # So we fill in a dummy argument at index 0
   for i in range(numOptions):
      n.append(int(stashItem["OptionCodes"][numOptions - 1 - i]))


   # All sections:
   if n[17] == 1:
      options["n17 = 1"] = "Item included for VAR reconfiguration"
      n[17] = 0       # Reset so that we don't get this message again.

   SectionForLookUp = stashItem["Section"]

   if stashItem["Section"] in (0, 31, 32, 33, 34):
      # These sections mostly share the option definitions, so
      # First set the SectionForLookUp to the smallest of these sections
      SectionForLookUp = 0
      # n2n1 is the Tracer Number, and make sure they don't show up later.
      if stashItem["Section"] in (33, 34):
         # These have three digit tracer numbers
         if 0 < n[3] * 100 + n[2]*10 + n[1]:
            options["Tracer"] = n[3] * 100 + n[2]*10 + n[1]
            # Reset the numbers
            n[1] = 0
            n[2] = 0
            n[3] = 0
      else:
         if 0 < n[2]*10 + n[1]:
            options["Tracer"] = n[2]*10 + n[1]
            # Reset the numbers
            n[1] = 0
            n[2] = 0

   # Assign the options using the stashOptionNames and stashOptionList dictionaries:
   for i in range(1, len(n)): # There is an unused n[0], so len(n) is large enough
      if n[i] != 0:                          # Not interested if 0
         # Calculate the keys to look up the values in the two dictionaries
         nNumber = SectionForLookUp*100 + i
         optionNumber = nNumber * 10 + n[i]
         try:
            # If there is an entry in both dictionaries, this should work.
            #options[stashOptionNames[nNumber]] = stashOptionList[optionNumber]
            options["n"+str(i).rjust(2)+" = "+str(n[i])] = stashOptionList[optionNumber]
         except:
            # Uups, it didn't. At least let the user know that there is an unknown option
            options['n' + str(i)] = str(n[i])

   return options

def printItem(stashItem):
   # This method prints all the information onto the screen.
   # It uses the Selector dictionary to print meaningful text instead of abstract values.
   print stashItem["Description"]

   print " ------- Fundamental Data ---------- "
   print "  Section ", stashItem["Section"], "     Item ", stashItem["Item"]
   print "  Model       : ", str(stashItem["Model"   ]).rjust(3), ModelSelector   [stashItem["Model"   ]]

   print " ------- Grid Data ----------------- "
   print "  Grid        : ", str(stashItem["Grid"    ]).rjust(3),  GridSelector    [stashItem["Grid"    ]]
   print "  Time        : ", str(stashItem["Time"    ]).rjust(3),  TimeSelector    [stashItem["Time"    ]]
   print "  Levels      : ", str(stashItem["LevelT"  ]).rjust(3),  LevelTSelector  [stashItem["LevelT"  ]]
   # If the level is not 5 (single level), the LevelF and LevelL give the first and last level of the range.
   # However, they too are coded, so for example 11 is not level 11, but actually the top level.
   if stashItem["LevelT"] == 5:        # Single level data
      if (stashItem["LevelF"] <> -1) or (stashItem["LevelL"] <> -1):
         print "WARNING: LevelF and LevelL should be set to -1, but are: ", stashItem["LevelF"], stashItem["LevelL"]
   else:
      print "    From      : ", str(stashItem["LevelF"  ]).rjust(3), LevelFLSelector[stashItem["LevelF"]]
      print "    To        : ", str(stashItem["LevelL"  ]).rjust(3), LevelFLSelector[stashItem["LevelL"]]

   print "  Pseudo      : ", str(stashItem["PseudoT" ]).rjust(3),  PseudoTSelector [stashItem["PseudoT" ]]
   if stashItem["PseudoT"] == 0:        # No Pseudo Levels
      if (stashItem["PseudoF"] <> 0) or (stashItem["PseudoL"] <> 0):
         print "WARNING: PseudoF and PseudoL should be set to 0, but are: ", stashItem["PseudoF"], stashItem["PseudoL"]
   else:
      print "    From      : ", str(stashItem["PseudoF" ]).rjust(3), PseudoFSelector[stashItem["PseudoF"]]
      print "    To        : ", str(stashItem["PseudoL" ]).rjust(3), PseudoLSelector[stashItem["PseudoL"]]
   print "  Halo        : ", str(stashItem["Halo"    ]).rjust(3), HaloSelector [stashItem["Halo"    ]]
   print "  Rotation    : ", str(stashItem["Rotate"  ]).rjust(3), RotateSelector[stashItem["Rotate" ]]

   print " ------- Data Data ---------------- "
   print "  Data Type   : ", str(stashItem["DataT"   ]).rjust(3), DataTSelector   [stashItem["DataT"   ]]
   print "  Space       : ", str(stashItem["Space"   ]).rjust(3), SpaceSelector   [stashItem["Space"   ]]
   if stashItem["Space"] == 7:         # Points to item in Section 0
      print "    points to Section 0, Item", stashItem["Point"]
   print "  Level Compr.: ", str(stashItem["LevCom"  ]).rjust(3), LevComSelector  [stashItem["LevCom"  ]]
   if stashItem["PC"] == [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99]:
      print "  Packing     :  -99 Never packed"
   else:
      print "  Packing     :"
      for i in range(10):
         pc = stashItem["PC"][i]
         print "    Stream", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A"][i], " : ", 
         if pc == -99:
            print "-99 not packed"
         else:
            print str(pc).rjust(3), "bits"

   options = analyseOptions(stashItem)
   if len(options) > 0:
      print " ------- Option Data -------------- "
      for key in options.keys():
         print " ", key.ljust(11), ": ", options[key]
   
   print " ------- Other Data --------------- "
   for element in ListOfAsYetUnwrittenElements:
      print " ", element.ljust(11), ": ", stashItem[element]

def main():
   # ------------------------------------------------------------------
   # Main routine, it gets called whenever the program starts with 
   # the right amount of parameters.
   # It brings with it a subroutine to run through a STASHmaster file and collect
   # STASH entries.
   def nextItem():
      #----------------------------------------------
      # NextItem routine returns the next stash item from
      # the file.
      # Method: read lines until one is found that starts with "1|", 
      # then split this, and the following 4, along the | marks.
      # Assign appropriately.
      stashItem = newStashItem()
      line = "    "
      while not line.startswith("1|"):
         line = file.readline()
         if len(line) == 0:
            print "Reached end of file."
            print "Didn't find the entry."
            sys.exit(3)
      # First Line
      lineItems = line.split("|")
      stashItem["Model"]   =  int(lineItems[1])
      stashItem["Section"] =  int(lineItems[2])
      stashItem["Item"]    =  int(lineItems[3])
      stashItem["Description"] =  lineItems[4].strip()
      # Second Line
      line = file.readline()
      lineItems = line.split("|")
      stashItem["Space"]   =  int(lineItems[ 1])
      stashItem["Point"]   =  int(lineItems[ 2])
      stashItem["Time"]    =  int(lineItems[ 3])
      stashItem["Grid"]    =  int(lineItems[ 4])
      stashItem["LevelT"]  =  int(lineItems[ 5])
      stashItem["LevelF"]  =  int(lineItems[ 6])
      stashItem["LevelL"]  =  int(lineItems[ 7])
      stashItem["PseudoT"] =  int(lineItems[ 8])
      stashItem["PseudoF"] =  int(lineItems[ 9])
      stashItem["PseudoL"] =  int(lineItems[10])
      stashItem["LevCom"]  =  int(lineItems[11])
      # Thrid Line
      line = file.readline()
      lineItems = line.split("|")
      stashItem["OptionCodes"] =  lineItems[1].strip()
      stashItem["VersionMask"] =  lineItems[2].strip()
      stashItem["Halo"]    =  int(lineItems[3])
      # Fourth line
      line = file.readline()
      lineItems = line.split("|")
      stashItem["DataT"]   =  int(lineItems[1])
      stashItem["DumpP"]   =  int(lineItems[2])
      stashItem["PC"] = []
      for pc in lineItems[3].strip().split():
         stashItem["PC"].append(int(pc))
      # Fifth and last line
      line = file.readline()
      lineItems = line.split("|")
      stashItem["Rotate"]  =  int(lineItems[1])
      stashItem["PPFC"]    =  int(lineItems[2])
      stashItem["User"]    =  int(lineItems[3])
      stashItem["LBVC"]    =  int(lineItems[4])
      stashItem["BLEV"]    =  int(lineItems[5])
      stashItem["TLEV"]    =  int(lineItems[6])
      stashItem["RBLevV"]  =  int(lineItems[7])
      stashItem["CFLL"]    =  int(lineItems[8])
      stashItem["CFFF"]    =  int(lineItems[9])
      return stashItem

   # Main routine again.

   # Get the parameters
   filename = sys.argv[1]
   stashitem = int(sys.argv[2])
   section = int(stashitem / 1000)
   item = stashitem - section * 1000
   print "Section: ", section, " Item: ", item

   # Open the file, exit on error.
   try:
      file = open(filename, 'r')
   except:
      print "Error opening file ", filename
      sys.exit(2)
   
   # Search through the file for the relevant stash item.
   stashItem = nextItem()
   while ((stashItem["Section"] <> section) or (stashItem["Item"] <> item)):
      stashItem = nextItem()
   
   # Display said item.
   printItem(stashItem)
   
   file.close()

def help():
   print """
   Help:
   
   please enter the file name of the STASHmaster file as first,
   and the section/item number as second argument.
   
   example:
   """
   print "   ", sys.argv[0], "MyUserSTASHmaster 34180"
   print """
   
   Hint: You can point to a leave-file, this program will recognise
         the STASHmaster section in it and ignore the rest.
   
   WARNING: You should not use this tool to check whether your own 
            STASHmaster entry is valid. This program might read the
            file differently than the UM.
   """

if __name__ == '__main__' :
   if ( len(sys.argv) == 3 ):
      main()
   else:
      help()
      sys.exit(1)
