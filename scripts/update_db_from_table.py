from os import stat
import geopandas as gpd
import pandas as pd
import shapely
from pyproj import Transformer
import numpy as np
from shapely.geometry import Point
import rasterio
import matplotlib.pyplot as plt
from collections import OrderedDict

def find_zone(lon):
    if lon > 132.:
        return 53
    else:
        return 52

def transform_coords(x,y,inProj, outProj):
    transformer = Transformer.from_crs(inProj, outProj, always_xy = True)
    return transformer.transform(x,y)

# paths to files
infile = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\github\csv\MORPH_Bores.csv"

df_bore = pd.read_csv(infile)

assert len(df_bore.MORPH_ID) == len(df_bore.MORPH_ID.unique())

# drop any creepy nan rows
df_bore.dropna(how='all', inplace=True)

schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('BoreName', 'str:200'), ('BoreReport', 'str:200'), ('HydroID', 'int'), ('HydroCode', 'str:30'), ('StateBoreID', 'str:50'),
         ('StatePipeID', 'str:30'), ('StateTerritory', 'str:6'), ('Agency', 'int'), ('WCode', 'int'), ('BoreDepth', 'float'), ('DrilledDepth', 'float'),
         ('Status', 'str:30'), ('DrilledDate', 'datetime'), ('HGUID', 'int'), ('HGUNumber', 'int'), ('HGUName', 'str:200'), ('NafHGUNumber', 'int'),
          ('AquiferType', 'int'), ('FType', 'str:50'), ('Latitude', 'float'), ('Longitude', 'float'), ('Easting', 'float'), ('Northing', 'float'),
          ('Projection', 'int'), ('ProjectionZone', 'int'), ('CoordMethod', 'str:30'), ('HeightDatum', 'str:30'), ('GALandElev', 'float'), ('GALandElevMethod', 'str:30'),
          ('RefElev', 'float'), ('RefElevDesc', 'str:30'), ('RefElevMethod', 'str:30'),
            ('basement_MD', 'float'), ('min_basement_MD', 'float'), ('basementGeol', "str:50"),
            ('basementRockType', 'str:50'), ('basementAgeTo', "str:50"), ('surfaceGeol', "str:80"),
            ('surfaceRepAge', "str:30"),('surfaceLith', "str:50"),
         ('FTypeClass', 'str:50'), ('ConstructionLog', 'int'), ('LithLog', 'int'), ('HydrostratLog', 'int'), ('HydroChem', 'int'),
                                     ('GAHydroChem', 'int'),
          ('AddedBy', 'str:20'), ('Comment', 'str:100'), ('Source', 'str:20'), ("QAQCd_By", 'str:20'), ('QAQC_date', 'datetime')]),
           'geometry': 'Point'}

cols = [c for c in schema['properties']] + ['geometry']

gdf_bore = gpd.read_file(r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\github\database\MORPH_Boreholes.gpkg", layer = "MORPH_Bores")

mask = []

for index, row in df_bore.iterrows():
    if not row['MORPH_ID'] in gdf_bore.MORPH_ID.values:
        mask.append(index)

df = df_bore.iloc[mask]

for index, row in df.iterrows():
    x, y = row['Easting'], row['Northing']
    lon, lat = row['Longitude'], row['Latitude']
    geom = row['geometry']
    # if all are nulls raise an error
    if np.all(pd.isnull([x, y, lon, lat])):
        print("Row {} is missing coordinate information".format(index))
        break
    # get the projection zone
    zone = row['ProjectionZone']
    if pd.isnull(zone):
        zone = find_zone(lon)
        df.at[index, 'ProjectionZone'] = zone
    if not pd.isnull(geom):
        # if not a string convert to point object
        if isinstance(row['geometry'], str):
            df.at[index, 'geometry'] = shapely.wkt.loads(row['geometry'])
    # if the geometry object doesn't exist, create it
    else:
        if not np.any(np.isnan([lon, lat])):
            newx, newy = transform_coords(lon, lat, "EPSG:4283", "EPSG:3577")
        else:
            newx, newy = transform_coords(x, y, "EPSG:283{}".format(zone), "EPSG:3577")
        df.at[index, 'geometry'] = Point(newx, newy)

    # now add the other coords if they are not present
    if np.any(np.isnan([x, y])):
        newx, newy = transform_coords(lon, lat, "EPSG:4283", "EPSG:283{}".format(zone))
        df.at[index, 'Easting'] = newx
        df.at[index, 'Northing'] = newy
    if np.any(np.isnan([lon, lat])):
        newlon, newlat = transform_coords(x, y, "EPSG:283{}".format(zone), "EPSG:4283")
        df.at[index, 'Longitude'] = newlon
        df.at[index, 'Latitude'] = newlat


# convert to a geodataframe so it can load into a geopackage
new_gdf = gpd.GeoDataFrame(df, geometry='geometry',crs = "EPSG:3577")

gdf_merged = gdf_bore.append(new_gdf)


morph_file = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\databases\MORPH_Boreholes.gpkg"

gdf_merged[cols].to_file(morph_file, layer='MORPH_Bores', driver="GPKG", schema = schema)