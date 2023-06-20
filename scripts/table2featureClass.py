import geopandas as gpd
import os

def joinAndExport(geodataframe):
    gdf_merged = gdf['']


infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores").to_crs("epsg:28352")

gdf['X'] = [g.x for g in gdf.geometry]
gdf['Y'] = [g.y for g in gdf.geometry]

gdf_bl = gpd.read_file(infile, layer='MORPH_BoreLog')
gdf_ll = gpd.read_file(infile, layer='MORPH_LithologyLog')
gdf_c = gpd.read_file(infile, layer='MORPH_ConstructionLog')

# join on the MORPH id







