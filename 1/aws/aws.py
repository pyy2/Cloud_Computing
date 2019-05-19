import boto3, uuid, csv

# Call s3 service
s3 = boto3.client('s3')

# Create bucket
bucket_name = 'cs1699-{}'.format(uuid.uuid4()) # Bucket name must be unique
print('Creating new bucket with name: {}'.format(bucket_name))
s3.create_bucket(Bucket=bucket_name, 
    CreateBucketConfiguration = {'LocationConstraint': 'us-east-2'}) # Set location

print("Creating Table")
# Get DyanmoDB resource
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table_name = 'cs1699data-{}'.format(uuid.uuid4())

# Create schema
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'provider',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'key',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'provider',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'key',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print('Success!')

# Open csv file and read data into table
print('Loading Data...')
with open('../Big3CloudProviders.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    for item in csvf:
        body = open('../Big3CloudProviders.csv', 'r')

        object_key = item[4].lstrip()
        print('Uploading some data to {} with key: {}'.format(
            bucket_name, object_key))

        s3.put_object(Bucket=bucket_name, Key=object_key, 
                Body = open('../logos/' + object_key, 'rb'))

        # Create a url of the object
        url = s3.generate_presigned_url(
            'get_object', {'Bucket': bucket_name, 'Key': object_key})
        print(url)

        metadata_item = {'provider': item[0], 'key': item[1], 
                 'year' : item[2], 'logoSize' : item[3], 'fileName': url} 
        try:
            table.put_item(Item=metadata_item)
        except:
            print("item may already be there or another failure")

# Creates an instance with table up until this point. When 'enter'
# is pressed, the table and bucket instance will be destroyed
try:
    input = raw_input
except NameError:
    pass
input("\nPress enter to continue...")

# First, create the service resource object
s3 = boto3.resource('s3')
# Now, the bucket object
bucket = s3.Bucket(bucket_name)

# Delete objects in bucket
print('\nDeleting all objects in bucket {}.'.format(bucket_name))
delete_responses = bucket.objects.delete()
for delete_response in delete_responses:
    for deleted in delete_response['Deleted']:
        print('\t Deleted: {}'.format(deleted['Key']))

# Delete table and bucket
table.delete()
bucket.delete()