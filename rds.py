import boto3
import sys
import argparse


def list_instances():
   client = boto3.client('rds')
   instances = client.describe_db_instances() 
   columns_format="%-3s %-20s %-60s %-12s %-7s %-8s %-8s %-12s %-12s"
   
   print(columns_format % ("num", "Identifier", "Endpoint Address", "Class", "Engine", "Version", "MultiAZ","Status","PublicIP")) 
   num = 1
   for n in range(len(instances.get('DBInstances'))):
      PA_access =  instances.get('DBInstances')[n].get('PubliclyAccessible')
      if PA_access:	
      	print(columns_format % (
                               num,
                               instances.get('DBInstances')[n].get('DBInstanceIdentifier'),
                               instances.get('DBInstances')[n].get('Endpoint').get('Address'),
                               instances.get('DBInstances')[n].get('DBInstanceClass'),
                               instances.get('DBInstances')[n].get('Engine'),
                               instances.get('DBInstances')[n].get('EngineVersion'),
                               instances.get('DBInstances')[n].get('MultiAZ'),
                               instances.get('DBInstances')[n].get('DBInstanceStatus'),
			       instances.get('DBInstances')[n].get('PubliclyAccessible')
                             )) 
      num = num + 1

def main():

    list_instances()

if __name__ == '__main__':
    sys.exit(main())



import boto3
from datatool import tools

client = boto3.client('rds')
rds_pub = ["num", "Identifier", "Endpoint Address", "Class", "Engine", "Version", "MultiAZ","Status","PublicIP"]

@tools.write_csv("RDS_public", rds_pub)

def list_instances():
   instances = client.describe_db_instances()
   s_no = 1

   for n in instances['DBInstances']:
        PA_access =  n['PubliclyAccessible']
        if PA_access:

            DB_instance_identifier = n['DBInstanceIdentifier']
            Endpoint_Address = n['Endpoint']['Address']
            class_i = n['DBInstanceClass']
            Engine = n['Engine']
            Version = n['EngineVersion']
            MultiAZ = n['MultiAZ']
            Status = n['DBInstanceStatus']
            PublicIP = n['PubliclyAccessible']
            yield([s_no,DB_instance_identifier,Endpoint_Address,class_i,Engine,Version,MultiAZ,Status,PublicIP]) 
            s_no = s_no + 1




list_instances()
