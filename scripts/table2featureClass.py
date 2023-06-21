import geopandas as gpd
import os
from collections import OrderedDict

def joinTables(geodataframe, cols):
    gdf_xyz = geodataframe.merge(gdf[cols], on = "MORPH_ID")
    # create geometry columns
    geometry = gpd.points_from_xy(gdf_xyz['Easting'], gdf_xyz['Northing'], gdf_xyz['TopElev'],
                                  crs = "epsg:28352")
    gdf_xyz['geometry'] = geometry
    gdf_xyz.set_crs("epsg:28352", inplace = True)
    return gdf_xyz


infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores").to_crs("epsg:28352")

gdf['Easting'] = [g.x for g in gdf.geometry]
gdf['Northing'] = [g.y for g in gdf.geometry]

bl_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'),
                                        ('Easting', 'float'), ('Northing', 'float'),
                                        ('FromDepth', 'float'), ('ToDepth', 'float'),
                                        ('TopElev', 'float'), ('BottomElev', 'float'), ('HGUID', 'int'),
                                        ('HGUNumber', 'int'), ('NafHGUNumber', 'int'),
                                        ('NafHGUName', 'str:255'), ('Description', 'str:255'),
                                        ('Author', 'str:50'), ('Source', 'str:100'), ('Comment', 'str:250'),
                                        ('GA_UNIT', 'str:30'), ('GA_STRATNO', 'int')
                                        ]), 'geometry': 'Point'}

bl_cols = [c for c in bl_schema['properties']] + ['geometry']
gdf_bl = gpd.read_file(infile, layer='MORPH_BoreLog')
gdf_bl_xyz = joinTables(gdf_bl, ['MORPH_ID', 'Easting', 'Northing'])
gdf_bl_xyz[bl_cols].to_file(infile, layer='MORPH_Borelog_XYZ', driver="GPKG", schema = bl_schema)

# To write to a geopackage, the dataframe needs to first be written as a geodataframe

ll_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'),
                                        ('Easting', 'float'), ('Northing', 'float'),
                                        ('FromDepth', 'float'), ('ToDepth', 'float'),
                                        ('TopElev', 'float'), ('BottomElev', 'float'), ('GALithType', 'str:50'),
                                        ('MajorLithCode', 'str:50'), ('MinorLithCode', 'str:50'),
                                        ('Description', 'str:255'), ('Source', 'str:100'),
                                        ('LogType', 'int')
                                        ]), 'geometry': 'Point'}

ll_cols = [c for c in ll_schema['properties']] + ['geometry']
gdf_ll = gpd.read_file(infile, layer='MORPH_LithologyLog')
gdf_ll_xyz = joinTables(gdf_ll, ['MORPH_ID', 'Easting', 'Northing'])
gdf_ll_xyz[ll_cols].to_file(infile, layer='MORPH_Lithologylog_XYZ', driver="GPKG", schema = ll_schema)

cl_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'),
                                        ('Easting', 'float'), ('Northing', 'float'),
                                        ('FromDepth', 'float'), ('ToDepth', 'float'),
                                        ('TopElev', 'float'), ('BottomElev', 'float'),
                                        ('ConstructionType', 'str:50'), ('Material', 'str:50'),
                                        ('InnerDiameter', 'float'), ('OuterDiameter', 'float'),
                                        ('Property', 'str:50'), ('PropertySize', 'float'),
                                        ('DrillMethod', 'str:50'), ('LogType', 'int')
                                        ]), 'geometry': 'Point'}

cl_cols = [c for c in cl_schema['properties']] + ['geometry']
gdf_cl = gpd.read_file(infile, layer='MORPH_ConstructionLog')
gdf_cl_xyz = joinTables(gdf_cl, ['MORPH_ID', 'Easting', 'Northing'])
gdf_cl_xyz[cl_cols].to_file(infile, layer='MORPH_ConstructionLog_XYZ', driver="GPKG", schema = cl_schema)











