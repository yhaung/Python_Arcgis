# Optimizing geospatial data with appropriate field lengths
# credit - Kyaw Naing Win, Ye Htet Aung, OneMap
import os

source_fc =r"D:\OMM_GIS\Projects\COVID_19\202005___Hospital_Distance_Analysis_step_for_OMM_MOHS_Anada\20200524_Hospital_Distance_Analysis_step_for_OMM_MOHS_Anada\MIMU_Layer\village_points_mimu\myanmar_village_points.shp"

out_path = r"D:\Temp\test"
out_name = os.path.basename(source_fc)
geometry_type = arcpy.Describe(target_fc).shapeType.upper()

# create a replicate file (empty)

target_fc = out_path+"\\"+out_name

arcpy.CreateFeatureclass_management (out_path, out_name, geometry_type)
arcpy.DeleteField_management (target_fc, "Id")

# extract schema from source

fields = arcpy.ListFields(source_fc)

schema = []

for field in fields:
    mylen =0
    if field.type == "Double" or field.type=="Float":
        schema.append([field.name,field.type,field.length, field.precision, field.scale])
    elif field.type=='String':
        for row in arcpy.da.SearchCursor(source_fc,field.name):
            len0 =len(row[0])
            if len0>mylen:
                mylen=len0
        
        schema.append([field.name,field.type,field.length,mylen])
    else:
        schema.append([field.name,field.type,field.length])
        

# create attribute table in target 

for index,item in enumerate(schema):
    if index>1:
        
        NAME = item[0]
        TYPE = item[1]
        LENGTH = int(item[2])
        if TYPE == "Double" or TYPE=="Float":
            PRECISION = int(item[3])
            SCALE = int(item[4])
            arcpy.AddField_management(target_fc,NAME,TYPE,field_precision=PRECISION,field_scale=SCALE,field_length=LENGTH,)
        if TYPE =='String':
            LENGTH =int(item[3])+0
            arcpy.AddField_management(target_fc,NAME,TYPE,field_length=LENGTH)
        else:
            
            arcpy.AddField_management(target_fc,NAME,TYPE,field_length=LENGTH)

 			
# copy features and attributes from source to target

arcpy.Append_management(source_fc,target_fc)

        
        