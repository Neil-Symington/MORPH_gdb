import geopandas as gpd
from gdbSchema import get_schema

infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores")

flags = {'ConstructionLog': "MORPH_ConstructionLog",
             'LithLog': "MORPH_LithologyLog",
             'HydrostratLog': "MORPH_BoreLog",
             'waterLevel': "MORPH_WaterLevels"}

for key, layer in flags.items():
    gdf_table = gpd.read_file(infile, layer = layer)
    mask = gdf.MORPH_ID.isin(gdf_table.MORPH_ID)
    gdf.at[mask, key] = 1
    gdf.at[~mask, key] = 0

mb_schema = get_schema("MORPH_Bores")

gdf.to_file(infile, layer='MORPH_Bores', driver="GPKG", schema = mb_schema)
