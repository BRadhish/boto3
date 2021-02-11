import boto3


client = boto3.client('elb')
client1 = boto3.client('elbv2')
def classic_lb():

    client = boto3.client('elb')

    response = client.describe_load_balancers()
    print( " %%%%%%%%%%%% Classic  Loadbalancer List %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    for describe in response['LoadBalancerDescriptions']:
        print("Load balancer name: " + describe['LoadBalancerName'])
        print("DNSName: " + describe['DNSName'])
        print("VPC ID : " , describe["VPCId"])
        print("AvailabilityZones : " , describe["AvailabilityZones"])
        print(" Subnet ID : ", describe["Subnets"])
        l_port = [x['Listener']['LoadBalancerPort'] for x in describe["ListenerDescriptions"]]
        print(" LoadBalancerPort : ", l_port)
        instance_port = [x['Listener']['InstancePort'] for x in describe["ListenerDescriptions"]]
        print(" InstancePort : ", instance_port)
        #ssl_cert = [x['Listener']["SSLCertificateId"] for x in describe["ListenerDescriptions"]]
        #print(" SSLCertificateId : ", ssl_cert)
        print("/////////////////////////////////////////")




def appnet_lb():



    response = client1.describe_load_balancers()

    print( " %%%%%%%%%%%% Application and Network Loadbalancer List %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    for lb_net in response['LoadBalancers']:
        print("LoadBalancerArn:   " + lb_net['LoadBalancerArn'])
        print("DNS name:  " + lb_net['DNSName'])
        print("LoadBalancerName:  " + lb_net['LoadBalancerName'])
        print("VpcId :  " + lb_net['VpcId'])
        print("IpAddressType:  ", lb_net['IpAddressType'])
        print("Load Balancer Type: ", lb_net['Type'])
        for i in lb_net["AvailabilityZones"]:
            print("Subnet ID :  " + i["SubnetId"])
            print("ZoneName: " + i["ZoneName"])
            print("///////////////////////////////////////////////////")


classic_lb()
appnet_lb()
