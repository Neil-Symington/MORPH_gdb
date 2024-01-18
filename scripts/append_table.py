import geopandas as gpd
import pandas as pd
import os, sys
import rasterio
import numpy as np

# if running locally
os.chdir('scripts')
sys.path.append(os.getcwd())
from gdbSchema import get_schema


infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores")

gdf_warburton = gpd.read_file(r"C:/Users/u77932/Documents/MORPH/data/boreholes/working/Warburton_mission_bores.gpkg",layer = "Warburton_mission_bores")

gdf_warburton['Completed'] = ''
gdf_warburton['waterLevel'] = 0
gdf_warburton['Completed'] = ''

gdf_export = gdf.append(gdf_warburton)

mb_schema = get_schema("MORPH_Bores")
cols = [c for c in mb_schema['properties']] + ['geometry']

gdf_export[cols].to_file(infile, layer='MORPH_Bores', driver="GPKG", schema = mb_schema)