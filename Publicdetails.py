import boto3
from datatool import tools

client = boto3.client('elb')
client1 = boto3.client('elbv2')
client2 = boto3.client('route53')
cf = boto3.client('cloudfront')
client3 = boto3.client('dynamodb')
client4 = boto3.client('dax')
ec2 = boto3.client('ec2')

#CSV Headers

c_lb = ["S.No","LB_Name","DNS","VPC","AZ","Subnet","LB_Port","Instance_Port"]
an_lb = ["S.No","LB-ARN","DNS_Name","LB_Name","VPC_ID","IP_AddressType","LB_Type","Subnet_ID","Zone_name"] 
route_53 = ["S.No","hostedzone_ID","Name","Caller_Ref","Resource_record","Private_zone","Domain_type","Resource_set"]
cloud_front = ["S.No","Domain_name","Distribution_ID","Certificate_Source","Status","ARN_id","Target_Origin-ID","Alias_IP"] 
Dynamo_DB = ["S.No","Table_Name"]
DAX_DB = ["S.No","ClusterName","Cluster_ARN","Total_nodes","Active_Nodes","Node_Type","Clus_END_Addres","Port","Subnet_group","IAM_ARN","NodeID","Node_Address","Node_ID_PORT"]
Pub_sub = ["S.No","Public_subnet"]
public_ip = ["S.No","Public_IP","Domain"]

@tools.write_csv("Classic_LB",c_lb)
def classic_lb():
    client = boto3.client('elb')
    s_no = 1
    response = client.describe_load_balancers()
    print( " Running  Classic  Loadbalancer List......")

    for describe in response['LoadBalancerDescriptions']:
        lb_name =  describe['LoadBalancerName']
        dns_name = describe['DNSName']
        vpc_id = describe["VPCId"]
        A_Zones =  describe["AvailabilityZones"]
        subnet = describe["Subnets"]
        lb_port = [x['Listener']['LoadBalancerPort'] for x in describe["ListenerDescriptions"]]
        instance_port = [x['Listener']['InstancePort'] for x in describe["ListenerDescriptions"]]
        yield([s_no,lb_name,dns_name,vpc_id,A_Zones,subnet,lb_port,instance_port]) 
        s_no = s_no + 1

        #ssl_cert = [x['Listener']["SSLCertificateId"] for x in describe["ListenerDescriptions"]]
        #print(" SSLCertificateId : ", ssl_cert)



@tools.write_csv("appnet_LB",an_lb)
def appnet_lb():
    s_no = 1
    response = client1.describe_load_balancers()
    print( " %%%%%%%%%%%% Application and Network Loadbalancer List %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    for lb_net in response['LoadBalancers']:
        LB_Arn = lb_net['LoadBalancerArn']
        DNS_name = lb_net['DNSName']
        L_B_Name = lb_net['LoadBalancerName']
        VpcId  = lb_net['VpcId']
        IP_Address_type = lb_net['IpAddressType']
        LB_Type = lb_net['Type']
        for i in lb_net["AvailabilityZones"]:
            subnet_id = i["SubnetId"]
            zone_name = i["ZoneName"]
        yield([s_no,LB_Arn,DNS_name,L_B_Name,VpcId,IP_Address_type,LB_Type,subnet_id,zone_name]) 
        s_no = s_no + 1

@tools.write_csv("PublicDomain",route_53)
def route53():
    s_no = 1
    instances = client2.list_hosted_zones_by_name(
    MaxItems='100'
    )
    print("***********List of Public accessible Hosted zones are listed here *********************")
    for pz in instances['HostedZones']:
        private_zone =  pz['Config']['PrivateZone']
        if not private_zone :
            ID = pz['Id']
            name_n =pz['Name']
            Caller_Reference = pz['CallerReference']
            Resource_RecordSetCount = pz['ResourceRecordSetCount']
            private_zone = pz['Config']['PrivateZone']
            records = client2.list_resource_record_sets(HostedZoneId = pz['Id'])
            Resource_Record = "|".join([_['Name'] for _ in records['ResourceRecordSets']])
            for domain in records['ResourceRecordSets']:
                Domain_type = domain['Type']
            yield([s_no,ID,name_n,Caller_Reference,Resource_RecordSetCount,private_zone,Domain_type,Resource_Record])
            s_no = s_no + 1


@tools.write_csv("cloud_front",cloud_front)
def cloudfront():
    s_no = 1
    distributions=cf.list_distributions()
    if distributions['DistributionList']['Quantity'] > 0:
        for distribution in distributions['DistributionList']['Items']:
            print("\n******************CloudFront Distributions :******************************")
            Domain_N = distribution['DomainName']
            Distribution_id = distribution['Id']
            Certificate_s = distribution['ViewerCertificate']['CertificateSource']
            status = distribution['Status']
            ARN_id = distribution['ARN']
            Target_OriginId = distribution['DefaultCacheBehavior']['TargetOriginId']
            for alias_icp in distribution["AliasICPRecordals"]:
                alias_ip = alias_icp["CNAME"]
        #if(distribution['ViewerCertificate']['CertificateSource'] == "acm"):
            #Cer_icate =  distribution['ViewerCertificate']['Certificate']
            yield([s_no,Domain_N,Distribution_id,Certificate_s,status,ARN_id,Target_OriginId,alias_ip]) 
    else:    
        print("Error - No CloudFront Distributions Detected.") 
        s_no = s_no + 1

@tools.write_csv("DynamoDB",Dynamo_DB)
def dynamo_table():
    s_no = 1
    list_t = client3.list_tables() 
    tittle = ("***************The list of tables in DynamoDb are****************")
    for table_name in list_t['TableNames']:
        table = table_name
        yield([s_no,table]) 
        s_no = s_no + 1 

@tools.write_csv("DynamoDAXDB",DAX_DB)
def dax_list():
    s_no = 1
    response = client4.describe_clusters()
    stri = ("***************DAX clusters details****************")
    for cluster_name in response['Clusters']:
        clster_name = cluster_name['ClusterName']
        Cluster_Arn = cluster_name['ClusterArn']
        Total_Nodes = cluster_name['TotalNodes']
        Active_Nodes = cluster_name['ActiveNodes']
        Node_Type = cluster_name['NodeType']
        Clus_Endpoint_Adds =  cluster_name["ClusterDiscoveryEndpoint"]["Address"]
        Port = cluster_name["ClusterDiscoveryEndpoint"]["Port"]
        Subnet_group = cluster_name['SubnetGroup']
        IAM_ARN = cluster_name['IamRoleArn']
        for node_id in cluster_name['Nodes']:
            Node_D = node_id['NodeId']
            Node_ID_add = node_id["Endpoint"]["Address"]
            Node_ID_port = node_id["Endpoint"]["Port"]
            yield([s_no,cluster_name,Cluster_Arn,Total_Nodes,Active_Nodes,Node_Type,Clus_Endpoint_Adds, Port,Subnet_group,IAM_ARN,Node_D,Node_ID_add, Node_ID_port])
            s_no = s_no + 1

@tools.write_csv("PublicSunet",Pub_sub)
def pub_subnet():
    s_no = 1
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
        subnet = subnetDict
        yield([s_no,subnet])
        s_no = s_no + 1

@tools.write_csv("PublicIP",public_ip)
def publicip_list():
    s_no = 1 
    client = boto3.client('ec2')
    print( " ****************List of public IP addresses associated with the account****************")
    addresses_dict = client.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        e_ip = eip_dict['PublicIp']
        Domain =  eip_dict['Domain']
        yield([s_no,e_ip,Domain])
    s_no = s_no + 1 
   # print( "Instance id: " + eip_dict['InstanceId'])
        #print( "Network interface id : " + eip_dict['NetworkInterfaceId'])



#Execution

classic_lb()
appnet_lb()
cloudfront()
dynamo_table()
dax_list()
pub_subnet()
publicip_list()
route53()
