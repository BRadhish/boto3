import boto3
client = boto3.client('ec2')

print( " ****************List of public IP addresses associated with the account****************")
addresses_dict = client.describe_addresses()
for eip_dict in addresses_dict['Addresses']:
    print(eip_dict['PublicIp'])
    print( "Domain: " +  eip_dict['Domain'])
    #print( "Instance id: " + eip_dict['InstanceId'])
    print( "Network interface id : " + eip_dict['NetworkInterfaceId'])
