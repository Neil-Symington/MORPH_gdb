from collections import OrderedDict

mb_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('BoreName', 'str:200'), ('BoreReport', 'str:200'),
                                        ('HydroID', 'int'), ('HydroCode', 'str:30'), ('StateBoreID', 'str:50'),
                                        ('StatePipeID', 'str:30'), ('StateTerritory', 'str:6'), ('Agency', 'int'),
                                        ('WCode', 'int'), ('BoreDepth', 'float'), ('DrilledDepth', 'float'),
                                        ('Status', 'str:30'), ('DrilledDate', 'datetime'), ('HGUID', 'int'),
                                        ('HGUNumber', 'int'), ('HGUName', 'str:200'), ('NafHGUNumber', 'int'),
                                        ('AquiferType', 'int'), ('FType', 'str:50'), ('Latitude', 'float'),
                                        ('Longitude', 'float'), ('Easting', 'float'), ('Northing', 'float'),
                                        ('Projection', 'int'), ('ProjectionZone', 'int'), ('CoordMethod', 'str:30'),
                                        ('HeightDatum', 'str:30'), ('GALandElev', 'float'), ('GALandElevMethod', 'str:30'),
                                        ('RefElev', 'float'), ('RefElevDesc', 'str:30'), ('RefElevMethod', 'str:30'),
                                        ('basement_MD', 'float'), ('min_basement_MD', 'float'), ('basementGeol', "str:50"),
                                        ('basementRockType', 'str:50'), ('basementAgeTo', "str:50"), ('surfaceGeol', "str:80"),
                                        ('surfaceRepAge', "str:30"),('surfaceLith', "str:50"),('FTypeClass', 'str:50'),
                                        ('ConstructionLog', 'int'), ('LithLog', 'int'), ('HydrostratLog', 'int'),
                                        ('HydroChem', 'int'), ("waterLevel", "int"), ('GAHydroChem', 'int'),
                                        ('AddedBy', 'str:20'), ('Comment', 'str:100'), ('Source', 'str:20'),
                                        ("QAQCd_By", 'str:20'), ('QAQC_date', 'datetime')]), 'geometry': 'Point'}


bl_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'), ('FromDepth', 'float'),
                                        ('ToDepth', 'float'),('TopElev', 'float'), ('BottomElev', 'float'), ('HGUID', 'int'),
                                        ('HGUNumber', 'int'), ('NafHGUNumber', 'int'),
                                        ('NafHGUName', 'str:255'), ('Description', 'str:255'),
                                        ('Author', 'str:50'), ('Source', 'str:100'), ('Comment', 'str:250'),
                                        ('GA_UNIT', 'str:30'), ('GA_STRATNO', 'int')
                                        ]), 'geometry': 'None'}


ll_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'), ('FromDepth', 'float'), ('ToDepth', 'float'),
                                        ('TopElev', 'float'), ('BottomElev', 'float'), ('GALithType', 'str:50'),
                                        ('MajorLithCode', 'str:50'),('MinorLithCode', 'str:50'), ('Description', 'str:255'),
                                        ('Source', 'str:100'), ('LogType', 'int'),
                                        ]), 'geometry': 'None'}


cl_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'), ('FromDepth', 'float'),
                                        ('ToDepth', 'float'), ('TopElev', 'float'), ('BottomElev', 'float'),
                                        ('ConstructionType', 'str:50'), ('Material', 'str:50'), ('InnerDiameter', 'float'),
                                         ('OuterDiameter', 'float'), ('Property', 'str:50'), ('PropertySize', 'float'),
                                        ('DrillMethod', 'str:50'), ('LogType', 'int')
                                        ]), 'geometry': 'None'}

wl_schema = {'properties': OrderedDict([('MORPH_ID', 'int'), ('HydroCode', 'str:30'), ('TopScreen', 'float'),
                                        ('BottomScreen', 'float'), ('RefElev', 'float'), ('RefElevDesc', 'str:30'),
                                        ('SWL', 'float'), ('rSWL', 'float'), ('Source', 'str:20'),
                                        ('measuredDate', 'datetime'), ('nScreens', 'int'),
                                        ]), 'geometry': 'None'}

schemas = {"MORPH_Bores": mb_schema,
           "MORPH_LithologyLog": ll_schema,
           "MORPH_ConstructionLog": cl_schema,
           "MORPH_BoreLog": bl_schema,
           "MORPH_WaterLevels": wl_schema}

def get_schema(table_name, make_xyz = False):
    try:
        schema = schemas[table_name]
        if make_xyz:
            schema['geometry'] = 'Point'
        return schema
    except KeyError:
        print("{} name not found".format(table_name))
