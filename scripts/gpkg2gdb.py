import os
import arcpy

outdir = r"databases"
outfile = "MORPH_boreholes.gdb"
arcpy.CreateFileGDB_management(outdir, outfile)

arcpy.conversion.FeatureClassToGeodatabase("main.MORPH_BORES", os.path.join(outdir, outfile))
# As far as I can tell the renaming will need to be done within the window

arcpy.conversion.TableToTable("main.MORPH_Borelog", os.path.join(outdir, outfile), "MORPH_Borelog")
arcpy.conversion.TableToTable("main.MORPH_LithologyLog", os.path.join(outdir, outfile), "MORPH_LithologyLog")
arcpy.conversion.TableToTable("main.MORPH_ConstructionLog", os.path.join(outdir, outfile), "MORPH_ConstructionLog")

arcpy.management.AddRelate("MORPH_Bores", "MORPH_ID", "MORPH_Borelog", "MORPH_ID", "bores2borelog", "ONE_TO_ONE")
arcpy.management.AddRelate("MORPH_Bores", "MORPH_ID", "MORPH_LithologyLog", "MORPH_ID", "bores2lithlog", "ONE_TO_ONE")
arcpy.management.AddRelate("MORPH_Bores", "MORPH_ID", "MORPH_ConstructionLog", "MORPH_ID", "bores2constructionlog", "ONE_TO_ONE")