import boto3

ec2 = boto3.client('ec2')

def pub_subnet():

    subnetDict = {}
    apicall = ec2.describe_route_tables()
    print ( " ***********List of public subnet associated with the account **********")
    for routeTable in apicall['RouteTables']:
            associations = routeTable['Associations']
            routes = routeTable['Routes']
            isPublic = False

            for route in routes:
                gid = route.get('GatewayId', '')
                if gid.startswith('igw-'):
                    isPublic = True

            if(not isPublic):
                continue

            for assoc in associations:
                subnetId = assoc.get('SubnetId', None)  # This checks for explicit associations, only
                if subnetId:
                    subnetDict[subnetId] = isPublic
    if subnetDict:
        print(subnetDict)



def publicip_list():

    client = boto3.client('ec2')

    print( " ****************List of public IP addresses associated with the account****************")
    addresses_dict = client.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        print(eip_dict['PublicIp'])
        print( "Domain: " +  eip_dict['Domain'])
   # print( "Instance id: " + eip_dict['InstanceId'])
        print( "Network interface id : " + eip_dict['NetworkInterfaceId'])



pub_subnet()
publicip_list()
