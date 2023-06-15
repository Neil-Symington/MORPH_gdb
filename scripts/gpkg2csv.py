import geopandas as gpd
import os

infile = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\databases\MORPH_Boreholes.gpkg"

outdir = "csv"

gdf = gpd.read_file(infile, layer = "MORPH_Bores")
gdf = gdf.sort_values(by = 'MORPH_ID')
gdf.to_csv(os.path.join(outdir, ".".join(['MORPH_Bores', "csv"])),index = False)

for lyr in ["MORPH_LithologyLog", "MORPH_BoreLog", "MORPH_ConstructionLog"]:
    gdf = gpd.read_file(infile, layer = lyr)
    gdf = gdf.sort_values(by = ['MORPH_ID', "FromDepth"])
    gdf.to_csv(os.path.join(outdir, ".".join([lyr, "csv"])),
               index = False)