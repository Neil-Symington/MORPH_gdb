import lasio
import geopandas as gpd
import pandas as pd
import os
import numpy as np

#os.chdir("scripts")

# Read the existing GeoPackage file
infile = r"..\database\MORPH_Boreholes.gpkg"

gdf = gpd.read_file(infile, layer = "MORPH_Bores").to_crs("epsg:28352")

# open petrel headers

df_headers = pd.read_csv(r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\Petrel\MORPH_headers.txt",
                         delimiter = '\t')

gdf_missing = gdf[~gdf.HydroCode.isin(df_headers.HydroCode.values)]

gdf_missing['X'] = [g.x for g in gdf_missing.geometry]
gdf_missing['Y'] = [g.y for g in gdf_missing.geometry]


cols = df_headers.columns
df_newheader = gdf_missing[cols]

df_newheader.to_csv(r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\Petrel\MORPH_new_headers_18July.txt",
                    sep = '\t', index = False)

gdf_lith = gpd.read_file(infile, layer = "MORPH_Lithologylog_XYZ")

gdf_lith['X'] = [g.x for g in gdf_lith.geometry]
gdf_lith['Y'] = [g.y for g in gdf_lith.geometry]

outdir = r"C:\Users\u77932\Documents\MORPH\data\boreholes\compilation\Petrel\lithology_las"

df_lithcodes = pd.read_csv(r"C:\Users\u77932\Documents\Petrel\galiths.csv")

lith_code = {}

for index, row in df_lithcodes.iterrows():
    lith_code[row.lithology] = row.code

# split the bores into seperate dataframes

bores = {}

for boreid in gdf_lith.HydroCode.unique():
    outfile = os.path.join(outdir, "{}.las".format(boreid))
    if os.path.exists(outfile):
        continue
    df_bore = gdf_lith[gdf_lith.HydroCode == boreid]

    if (len(df_bore.GALithType.unique()) == 1) and (df_bore.GALithType.unique() == ["unk"]):
        pass
    else:
        bores[boreid] = df_bore

# now we want to interpolate each bore onto a constant depth interval
interval = 0.5

for boreid in sorted(bores.keys()):
    outfile = os.path.join(outdir, "{}.las".format(boreid))
    if os.path.exists(outfile):
        continue
    df_bore = bores[boreid]
    outfile2 = os.path.join(outdir, "{}.las".format(str(int(df_bore['MORPH_ID'].unique()[0]))))
    if os.path.exists(outfile2):
        continue
    depthTop = df_bore.FromDepth.values
    depthBottoms = df_bore.ToDepth.values

    df_newbore = pd.DataFrame(data = {'depths': [], "GALithType":[], "LithCode": []})

    df_newbore['depths'] = np.arange(depthTop.min(), depthBottoms.max(), interval)


    for index, row in df_bore.iterrows():
        mask = np.logical_and(df_newbore['depths'] >= row.FromDepth, df_newbore['depths'] <= row.ToDepth)
        inds = df_newbore[mask].index
        df_newbore.at[inds, "GALithType"] = row.GALithType

        try:
            df_newbore.at[inds, "LithCode"] = lith_code[row.GALithType]
        except KeyError:
            print(row.GALithType)
            df_newbore.at[inds, "LithCode"] = lith_code['unk']

    df_newbore = df_newbore[df_newbore.depths > 0]
    # write it to las
    las = lasio.LASFile()

    las.params['LMF'] = lasio.HeaderItem('LMF', value='GL')
    las.well['WELL'] = lasio.HeaderItem('WELL', value = df_bore['HydroCode'].unique()[0])
    las.well['UWI'] = lasio.HeaderItem('UWI', value = str(int(df_bore['MORPH_ID'].unique()[0])))
    las.well['X'] = lasio.HeaderItem('X', value = np.round(df_bore.X.values[0], 1), unit = 'm',
                                     descr = 'X OR EAST-WEST ORDINATE')
    las.well['Y'] = lasio.HeaderItem('Y', value = np.round(df_bore.Y.values[0], 1), unit = 'm',
                                     descr = 'Y OR NORTH-SOUTH ORDINATE')
    las.well['HZCS'] = lasio.HeaderItem('HZCS', value = 'GDA94 / MGA zone 52', descr = 'PROJECTED COORDINATE')

    las.add_curve('DEPT', np.round(df_newbore['depths'].values,2), unit='m')

    las.add_curve('Lithologies', df_newbore['LithCode'].values.astype(int).astype(str), descr = "GA lithology code")
    #las.add_curve('GALithType', df_newbore['GALithType'].values, descr = "GA litholgy type")

    #outfile = os.path.join(outdir, "{}.las".format(str(int(df_bore['HydroID'].unique()[0]))))
    las.write(outfile2, version = 2.0,len_numeric_field=-1)
