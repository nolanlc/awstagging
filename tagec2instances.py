######################################################################
#
# tagec2instances.py
#
# This Python script will read a CSV file and tag EC2 instances
# with map-migrated equal to specified ServerID values.
#
# To Use:
# Specify the S3 bucket name that the CSV file is located 
# along with the CSV filename.  
#
####################################################################

import boto3
import csv
import codecs

bucketname = 'cur-bucket-790232282124'
filename = 'instances-input112pm.csv'


def tag_ec2_instance(instance_id, tag_key, tag_value):
    ec2_client = boto3.client('ec2')
    try:
        tag_create = ec2_client.create_tags(
            Resources = [instance_id],
            Tags = [
                {
                    'Key' : tag_key,
                    'Value' : tag_value
                }])
    except:
        print ("Error Tagging instance_id: "+ instance_id)
    #print ("Return status: " + str(tag_create['ResponseMetadata']['HTTPStatusCode']))
    

def read_tag_csv_from_s3(bucketname, filename):
    client = boto3.client("s3")
    try:
        data  = client.get_object(Bucket=bucketname, Key=filename)
    
        for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
            instance_id = row['ID']
            serverID = row['ServerID']
            output = ("Tagging instance_id:" + instance_id + " with ServerID:"+serverID)
            print(output)
            
            #tag the instance
            tag_key = 'map-migrated'
            tag_value = serverID
            tag_ec2_instance(instance_id, tag_key, tag_value)
            
    except :
        msg = "error reading input file from S3 bucket: '" + bucketname + "/" + filename + "'"
        print(msg)

read_tag_csv_from_s3(bucketname, filename)

print ("Program complete.")