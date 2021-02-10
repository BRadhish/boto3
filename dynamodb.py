import boto3

def dynamo_table():
    client = boto3.client('dynamodb')
    list_t = client.list_tables()
    
    tittle = ("***************The list of tables in DynamoDb are****************")
    print(tittle.title())
    for table_name in list_t['TableNames']:
        print(table_name)


    list_dl = client.describe_limits()
    print( "*************The Describe limit details**************")

    print(list_dl)
    print("///////////////////////////////////////////////////////////")


def dax_list():
    client1 = boto3.client('dax')
    response = client1.describe_clusters()
    stri = ("***************DAX clusters details****************")
    print(stri.title())
    for cluster_name in response['Clusters']:
        print("The cluster name: " + cluster_name['ClusterName'])
        print("ClusterArn: " + cluster_name['ClusterArn'])
        print("TotalNodes: " , cluster_name['TotalNodes'])
        print("ActiveNodes: " , cluster_name['ActiveNodes'])
        print("NodeType: " + cluster_name['NodeType'])
        print("Cluster Endpoint Address: " + cluster_name["ClusterDiscoveryEndpoint"]["Address"])
        print("Port : " , cluster_name["ClusterDiscoveryEndpoint"]["Port"])
        print("Subnet group : " + cluster_name['SubnetGroup'])
        print("IAM ARN : " + cluster_name['IamRoleArn'])
        for node_id in cluster_name['Nodes']:
            print("Node ID : " , node_id['NodeId'])
            print("Node ID address: " + node_id["Endpoint"]["Address"])
            print("Node ID port: " , node_id["Endpoint"]["Port"])
        print("///////////////////////////////////////////////////////////")




dynamo_table()
dax_list()
