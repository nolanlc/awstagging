####################################################################
#
# getec2instances.py
#
# This Python script uses boto3 to get list of EC2 Instances in a Region
# and output it's Instance_ID, Instance_Type, Name and ServerID (if available) to 
# a CSV file.  It then uploads the CSV file to a specified S3 bucket.
#
# Users can add/change the ServerID column for each Instance and upload to S3.
# Run 'tagec2instances.py' to tag EC2 instances with assigned ServerIDs.  
#
# To use:
# Specify filename for CSV file.
# Specify S3 bucket name to upload CSV file.
#
#####################################################################
import boto3


filename = 'instances110pm.csv'  
bucket_name = "cur-bucket-790232282124"

def get_ec2_instances(filename):
    
    ec2 = boto3.resource('ec2')
    
    f = open(filename,'w')
    header = "ID,Instance_type,Name,ServerID\n"
    
    f.write(header)
    
    #Loop through all EC2 instances in the Region
    for instance in ec2.instances.all():
        
        instance_metadata = str(
        "Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\n".format(
             instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state)
         ) +"\n"
         
        instance_id =  instance.id
        instance_type = instance.instance_type
        #print(instance_id)
       
        instance_name = ""
        server_id = ""
        ec2instance = ec2.Instance(instance_id)
        
        tags = ec2instance.tags
        if tags != None:

            print ("Tags found for Instance ID: "+ instance_id)
            for tag in tags:
                if tag['Key'] == "Name":
                    instance_name = tag['Value']
                elif tag['Key'] == "map-migrated":
                    server_id = tag['Value']

        else :
            print ("No tags found for Instance ID: "+ instance_id)

        output = instance_id + "," + instance_type + "," + instance_name + "," + server_id +  "\n"
        print (output)
        f.write(output)

    f.close()   


def upload_file(file_name, bucket, object_name=None):
    print ("Hello Upload!")
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name,bucket,object_name)
    except ClientError as e:
        return False
    return True
    
   
get_ec2_instances(filename)


object_name = filename
upload_file(filename, bucket_name, object_name)

print ("Program complete")
     