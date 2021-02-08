import boto3

client = boto3.client('dynamodb')
list_t = client.list_tables()
for i in list_t['TableNames']:

    print(i)


list_dl = client.describe_limits()
print(list_dl)
