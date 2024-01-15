import geopandas as gpd
import os, sys
# if running locally
os.chdir('scripts')
sys.path.append(os.getcwd())
from gdbSchema import get_schema


def get_MORPH_ID(state, easting, northing):
    MID = ""
    state_lookup = {"WA": 5, "SA": 3, "NT": 7}
    assert state in state_lookup.keys()
    MID += str(state_lookup[state])
    easting_string, northing_string = str(easting), str(northing)
    MID += easting_string.split(".")[0][-4:]
    MID += northing_string.split(".")[0][-4:]
    MID += "1"
    MORPH_ID = int(MID)
    while MORPH_ID in gdf.MORPH_ID.values:
        MORPH_ID += 1
    return MORPH_ID

infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores")

mask = gdf.MORPH_ID < 1000000000

gdf_noMID = gdf[mask]

for index, row in gdf_noMID.iterrows():
    x,y = row['Easting'], row['Northing']
    state = row['StateTerritory']
    morph_id = get_MORPH_ID(state, x, y)
    gdf.at[index, 'MORPH_ID'] = morph_id

mb_schema = get_schema("MORPH_Bores")
cols = [c for c in mb_schema['properties']] + ['geometry']

gdf[cols].to_file(infile, layer='MORPH_Bores', driver="GPKG", schema = mb_schema)