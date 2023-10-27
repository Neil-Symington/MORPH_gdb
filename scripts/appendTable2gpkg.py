import geopandas as gpd
import os
from scripts.gdbSchema import get_schema
import pandas as pd

# Read the existing GeoPackage file
infile = r"..\database\MORPH_Boreholes.gpkg"

#gdf_lith = gpd.read_file(infile, layer = "MORPH_LithologyLog")
gdf_wl = gpd.read_file(infile, layer = "MORPH_WaterLevels")
ind_col = list(gdf_wl['MORPH_ID'].astype(str) + gdf_wl['SWL'].round(2).astype(str))
#ind_col = list(gdf_lith['MORPH_ID'].astype(str) + gdf_lith['FromDepth'].astype(str))
#gdf_constr = gpd.read_file(infile, layer = "MORPH_ConstructionLog")

# Read the CSV file
#csv_path = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\staging\construction2add.csv"
csv_path = "..\csv\MORPH_WaterLevels.csv"
df_csv = pd.read_csv(csv_path)
df_csv['indcol'] = df_csv['MORPH_ID'].astype(str) + df_csv['SWL'].round(2).astype(str)

# find rows that are not in the csv
for index, row in df_csv.iterrows():
    if not row['indcol'] in ind_col:
        gdf_wl = gdf_wl.append(df_csv.iloc[index])


# Write the updated GeoPackage file
#cl_schema = get_schema("MORPH_ConstructionLog")
#ll_schema = get_schema("MORPH_LithologyLog")
#ll_cols = [c for c in ll_schema['properties']] + ['geometry']
#gdf_lith[ll_cols].to_file(infile, layer = "MORPH_LithologyLog", driver="GPKG", schema = ll_schema)

wl_schema = get_schema("MORPH_WaterLevels")
wl_cols = [c for c in wl_schema['properties']] + ['geometry']
gdf_wl[wl_cols].to_file(infile, layer = "MORPH_WaterLevels", driver="GPKG", schema = wl_schema)