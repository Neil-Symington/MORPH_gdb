import geopandas as gpd
import sys, os
import pandas as pd

import pandas as pd

sys.path.append(r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\github\scripts")
os.chdir(r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\github\scripts")
from gdbSchema import get_schema

def joinTables(geodataframe, cols, z_col):
    gdf_xyz = geodataframe.merge(gdf_ss_z52[cols], on = "MORPH_ID")
    # create geometry columns
    geometry = gpd.points_from_xy(gdf_xyz['Easting'], gdf_xyz['Northing'], gdf_xyz[z_col],
                                  crs = "epsg:28352")
    gdf_xyz['geometry'] = geometry
    gdf_xyz.set_crs("epsg:28352", inplace = True)
    return gdf_xyz


polygon = gpd.read_file(r"C:\Users\u77932\Documents\MORPH\data\Extents\Musgrave_pv_project_outline_final.shp").to_crs("epsg:3577").iloc[0].geometry.buffer(5000)

morph_file = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(morph_file, layer = "MORPH_Bores")
mask = gdf.within(polygon)

gdf_ss = gdf[mask]

schema = get_schema("MORPH_Bores")

cols = [c for c in schema['properties']]  +  ['geometry']

gdf_ss[cols].to_file(morph_file, layer='MORPH_Bores', driver="GPKG", schema = schema)

# now iterate through other tables and only keep bores in gdf_ss

gdf_ss_z52 = gdf_ss.to_crs("epsg:28352")

gdf_ss_z52['Easting'] = [g.x for g in gdf_ss_z52.geometry]
gdf_ss_z52['Northing'] = [g.y for g in gdf_ss_z52.geometry]

bl_schema = get_schema("MORPH_BoreLog", make_xyz = True)

bl_cols = [c for c in bl_schema['properties']] + ['geometry']
gdf_bl = gpd.read_file(morph_file, layer='MORPH_BoreLog')

mask = gdf_bl.MORPH_ID.isin(gdf_ss.MORPH_ID)

gdf_bl = gdf_bl[mask]

gdf_bl_xyz = joinTables(gdf_bl, ['MORPH_ID', 'Easting', 'Northing'], z_col = "TopElev")
gdf_bl_xyz[bl_cols].to_file(morph_file, layer='MORPH_Borelog_XYZ', driver="GPKG", schema = bl_schema)

# To write to a geopackage, the dataframe needs to first be written as a geodataframe

ll_schema = get_schema("MORPH_LithologyLog", make_xyz = True)

ll_cols = [c for c in ll_schema['properties']] + ['geometry']
gdf_ll = gpd.read_file(morph_file, layer='MORPH_LithologyLog')

mask = gdf_ll.MORPH_ID.isin(gdf_ss.MORPH_ID)

gdf_ll = gdf_ll[mask]

gdf_ll_xyz = joinTables(gdf_ll, ['MORPH_ID', 'Easting', 'Northing'], z_col = "TopElev")
gdf_ll_xyz[ll_cols].to_file(morph_file, layer='MORPH_Lithologylog_XYZ', driver="GPKG", schema = ll_schema)

cl_schema = get_schema("MORPH_ConstructionLog", make_xyz = True)

cl_cols = [c for c in cl_schema['properties']] + ['geometry']
gdf_cl = gpd.read_file(morph_file, layer='MORPH_ConstructionLog')

mask = gdf_cl.MORPH_ID.isin(gdf_ss.MORPH_ID)

gdf_cl = gdf_cl[mask]

gdf_cl_xyz = joinTables(gdf_cl, ['MORPH_ID', 'Easting', 'Northing'], z_col = "TopElev")
gdf_cl_xyz[cl_cols].to_file(morph_file, layer='MORPH_ConstructionLog_XYZ', driver="GPKG", schema = cl_schema)

wl_schema = get_schema("MORPH_WaterLevels", make_xyz = True)

wl_cols = [c for c in wl_schema['properties']] + ['geometry']
gdf_wl = gpd.read_file(morph_file, layer='MORPH_WaterLevels')

mask = gdf_wl.MORPH_ID.isin(gdf_ss.MORPH_ID)

gdf_wl = gdf_wl[mask]
gdf_wl_xyz = joinTables(gdf_wl, ['MORPH_ID', 'Easting', 'Northing'], z_col = "rSWL")
gdf_wl_xyz[wl_cols].to_file(morph_file, layer='MORPH_WaterLevles_XYZ', driver="GPKG", schema = wl_schema)

# now filter the petrel files

infile = r"C:\Temp\test_well_heads"
outfile = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\Petrel\MORPH_heads_9Nov.dat"

with open(infile, 'r') as f:
    with open(outfile, 'w') as outf:
        header = True
        for line in f:
            if header:
                outf.write(line)
                if line.strip() == 'END HEADER':
                    header = False
            else:
                MID = line.split('"')[3]

                if int(MID) in gdf_ss.MORPH_ID.values:
                    outf.write(line)


infile = r"C:\Temp\MORPH_d2b"
outfile = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\Petrel\MORPH_well_heads_9Nov.dat"

with open(infile, 'r') as f:
    with open(outfile, 'w') as outf:
        header = True
        for line in f:
            if header:
                outf.write(line)
                if line.strip() == 'END HEADER':
                    header = False
            else:
                hydrocode = line.split('"')[3]

                if hydrocode in gdf_ss.HydroCode.values:
                    outf.write(line)


