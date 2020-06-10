# Optimizing geospatial data with appropriate field lengths
# credit - Kyaw Naing Win, Ye Htet Aung, OneMap
import os

source_fc = arcpy.GetParameterAsText(0)

out_path = arcpy.GetParameterAsText(1)

out_name = os.path.basename(source_fc)
geometry_type = arcpy.Describe(source_fc).shapeType.upper()

arcpy.CreateFeatureclass_management (out_path, out_name, geometry_type)


target_fc = out_path+"\\"+out_name

fields = arcpy.ListFields(source_fc)

schema = []
# extract schema from source
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

arcpy.DeleteField_management (target_fc, "Id") 			
# copy features and attributes from source to target
arcpy.Append_management(source_fc,target_fc)

        