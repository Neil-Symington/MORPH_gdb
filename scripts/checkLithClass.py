import geopandas as gpd
import yaml
import os

os.chdir("scripts")


# Read the existing GeoPackage file
infile = r"..\database\MORPH_Boreholes.gpkg"

gdf_lith = gpd.read_file(infile, layer = "MORPH_LithologyLog")

with open('lithMapping.yaml') as file:

    lithologyMapping = yaml.load(file, Loader=yaml.FullLoader)['lithologyMapping']


for lith in gdf_lith['GALithType'].unique():
    if not lith in lithologyMapping.keys():
        print(lith)