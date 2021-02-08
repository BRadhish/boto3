import boto3


cf = boto3.client('cloudfront')

print("\nCloudFront Distributions:\n")
distributions=cf.list_distributions()
if distributions['DistributionList']['Quantity'] > 0:
  for distribution in distributions['DistributionList']['Items']:
    print("Domain: " + distribution['DomainName'])
    print("Distribution Id: " + distribution['Id'])
    print("Certificate Source: " + distribution['ViewerCertificate']['CertificateSource'])
    print("status: " + distribution['Status'])
    print("ARN: " + distribution['ARN'])
    print("TargetOriginId:  " + distribution['DefaultCacheBehavior']['TargetOriginId'])
    for alias_icp in distribution["AliasICPRecordals"]:
        print("Aliasip:  " + alias_icp["CNAME"])
    if (distribution['ViewerCertificate']['CertificateSource'] == "acm"):
        print("Certificate: " + distribution['ViewerCertificate']['Certificate'])
else:    
  print("Error - No CloudFront Distributions Detected.") 
 
