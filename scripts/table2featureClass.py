import geopandas as gpd
from gdbSchema import get_schema

def joinTables(geodataframe, cols, z_col):
    gdf_xyz = geodataframe.merge(gdf[cols], on = "MORPH_ID")
    # create geometry columns
    geometry = gpd.points_from_xy(gdf_xyz['Easting'], gdf_xyz['Northing'], gdf_xyz[z_col],
                                  crs = "epsg:28352")
    gdf_xyz['geometry'] = geometry
    gdf_xyz.set_crs("epsg:28352", inplace = True)
    return gdf_xyz


infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores").to_crs("epsg:28352")

gdf['Easting'] = [g.x for g in gdf.geometry]
gdf['Northing'] = [g.y for g in gdf.geometry]

bl_schema = get_schema("MORPH_BoreLog", make_xyz = True)

bl_cols = [c for c in bl_schema['properties']] + ['geometry']
gdf_bl = gpd.read_file(infile, layer='MORPH_BoreLog')
gdf_bl_xyz = joinTables(gdf_bl, ['MORPH_ID', 'Easting', 'Northing'], z_col = "TopElev")
gdf_bl_xyz[bl_cols].to_file(infile, layer='MORPH_Borelog_XYZ', driver="GPKG", schema = bl_schema)

# To write to a geopackage, the dataframe needs to first be written as a geodataframe

ll_schema = get_schema("MORPH_LithologyLog", make_xyz = True)

ll_cols = [c for c in ll_schema['properties']] + ['geometry']
gdf_ll = gpd.read_file(infile, layer='MORPH_LithologyLog')
gdf_ll_xyz = joinTables(gdf_ll, ['MORPH_ID', 'Easting', 'Northing'], z_col = "TopElev")
gdf_ll_xyz[ll_cols].to_file(infile, layer='MORPH_Lithologylog_XYZ', driver="GPKG", schema = ll_schema)

cl_schema = get_schema("MORPH_ConstructionLog", make_xyz = True)

cl_cols = [c for c in cl_schema['properties']] + ['geometry']
gdf_cl = gpd.read_file(infile, layer='MORPH_ConstructionLog')
gdf_cl_xyz = joinTables(gdf_cl, ['MORPH_ID', 'Easting', 'Northing'], z_col = "TopElev")
gdf_cl_xyz[cl_cols].to_file(infile, layer='MORPH_ConstructionLog_XYZ', driver="GPKG", schema = cl_schema)

wl_schema = get_schema("MORPH_WaterLevels", make_xyz = True)

wl_cols = [c for c in wl_schema['properties']] + ['geometry']
gdf_wl = gpd.read_file(infile, layer='MORPH_WaterLevels')
gdf_wl_xyz = joinTables(gdf_wl, ['MORPH_ID', 'Easting', 'Northing'], z_col = "rSWL")
gdf_wl_xyz[wl_cols].to_file(infile, layer='MORPH_WaterLevles_XYZ', driver="GPKG", schema = wl_schema)











