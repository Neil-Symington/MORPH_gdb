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

df_tds = pd.read_csv(r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\staging\MORPH_TDS.csv")

gdf_merged = gdf.merge(df_tds[['MORPHID','TDSc_mg_L']],
                       left_on = 'MORPH_ID', right_on = 'MORPHID', how = 'left')

# do a quick compare
mask = np.all(pd.isnull(gdf_merged[['TDSc_mg_L', 'TDS_mgL-1']]), axis = 1)

gdf_compare = gdf_merged[~mask][['TDSc_mg_L', 'TDS_mgL-1']]

# replace the columnn
gdf_merged.drop('TDS_mgL-1', axis = 1,inplace = True)
gdf_merged.rename(columns = {'TDSc_mg_L': 'TDS_mgL-1'}, inplace = True)


mb_schema = get_schema("MORPH_Bores")
cols = [c for c in mb_schema['properties']] + ['geometry']

gdf_merged[cols].to_file(infile, layer='MORPH_Bores', driver="GPKG", schema = mb_schema)