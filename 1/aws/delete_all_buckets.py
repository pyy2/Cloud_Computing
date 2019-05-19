import boto3

# Call s3 service
s3 = boto3.client('s3')

# List buckets created
list_buckets_resp = s3.list_buckets()

# Create service resource object
s3 = boto3.resource('s3')

for bucket in list_buckets_resp['Buckets']:
    print('\nDeleting all objects in bucket {}.'.format(bucket))
    delete_responses = bucket.objects.delete()
    for delete_response in delete_responses:
        for deleted in delete_response['Deleted']:
            print('\t Deleted: {}'.format(deleted['Key']))
    bucket.delete()
