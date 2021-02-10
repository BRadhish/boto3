

import boto3

def dynamo_table():
    client = boto3.client('dynamodb')
    list_t = client.list_tables()
    print("***************The list of tables in DynamoDb are****************")
    for i in list_t['TableNames']:
        print(i)


    list_dl = client.describe_limits()
    print( "*************The Describe limit details**************")
    print(list_dl)
    print("///////////////////////////////////////////////////////////")


def dax_list():
    client1 = boto3.client('dax')
    response = client1.describe_clusters()
    print("***************DAX clusters details****************")
    for cluster_name in response['Clusters']:
        print("The cluster name: " + cluster_name['ClusterName'])
        print("ClusterArn: " + cluster_name['ClusterArn'])
        print("TotalNodes: " , cluster_name['TotalNodes'])
        print("ActiveNodes: " , cluster_name['ActiveNodes'])
        print("NodeType: " + cluster_name['NodeType'])
        print("Cluster Endpoint Address: " + cluster_name["ClusterDiscoveryEndpoint"]["Address"])
        print("Port : " , cluster_name["ClusterDiscoveryEndpoint"]["Port"])
        print("///////////////////////////////////////////////////////////")




dynamo_table()
dax_list()
