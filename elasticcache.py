import boto3

def elastic_cache():

    client = boto3.client('elasticache')
    response = client.describe_cache_clusters(
    )
    hosted_zone_id = []
    print(" **********List of Redis cluster are*********")
    for cache_clus in response['CacheClusters']:
        print("Cache cluster id:  " + cache_clus['CacheClusterId'])
        print("Engine version:  " + cache_clus['EngineVersion'])
        print("Engine name:  " + cache_clus['Engine'])
        print("Downloadlandingpage:  " + cache_clus['ClientDownloadLandingPage'])
        print("No of cache nodes: " , cache_clus['NumCacheNodes'])
        print("Preferred AZ: " + cache_clus['PreferredAvailabilityZone'])
        print("subnet group name: " + cache_clus['CacheSubnetGroupName'])
        response = client.describe_cache_subnet_groups(
                CacheSubnetGroupName = cache_clus['CacheSubnetGroupName']
                )
        for cache_subnet in response['CacheSubnetGroups']:
            print("Cache subnet group name:  " + cache_subnet['CacheSubnetGroupName'])
            print( "VPC ID : " + cache_subnet['VpcId'])
        for i in cache_subnet['Subnets']:
            print( "Subnets identifier  : " + i['SubnetIdentifier'])
            hosted_zone_id.append(i['SubnetIdentifier'])


        for j in cache_subnet['Subnets']:
            print("Subnet availability zone : " + j['SubnetAvailabilityZone']['Name'])
        print("/////////////////////////////////////////////////////////////////////////////")



def find_public_subnet():
    ec2 = boto3.client('ec2')
