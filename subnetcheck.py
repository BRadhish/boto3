import boto3

ec2 = boto3.client('ec2')

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
