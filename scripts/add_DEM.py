import geopandas as gpd
import pandas as pd
import os, sys
import rasterio
from pyproj import Transformer


# if running locally
os.chdir('scripts')
sys.path.append(os.getcwd())
from gdbSchema import get_schema


infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores")

lon_mask = pd.isnull(gdf.Longitude)

gdf_noLong = gdf[lon_mask]

for index, row in gdf_noLong.to_crs("4283").iterrows():
    lon, lat = row.geometry.x, row.geometry.y
    gdf.at[index, 'Longitude'] = lon
    gdf.at[index, 'Latitude'] = lat

mask = pd.isnull(gdf.GALandElev)

gdf_noDEM = gdf[mask]

dem_path = r"C:\Users\u77932\Documents\MORPH\data\elevation\Musgraves_SRTM_1SDEM_GDA94.tif"

src = rasterio.open(dem_path)
elevs = [v[0] for v in src.sample(gdf_noDEM[['Longitude','Latitude']].values)]


gdf_noDEM['GALandElev'] = elevs
gdf_noDEM['GALandElevMethod'] = 'DEM'

for index, row in gdf_noDEM.iterrows():
    GALandElev, GALandElevMethod = row.GALandElev, row.GALandElevMethod
    gdf.at[index, 'GALandElev'] = GALandElev
    gdf.at[index, 'GALandElevMethod'] = GALandElevMethod

mb_schema = get_schema("MORPH_Bores")
cols = [c for c in mb_schema['properties']] + ['geometry']

gdf[cols].to_file(infile, layer='MORPH_Bores', driver="GPKG", schema = mb_schema)