from gcloud import datastore
from gcloud import storage
import csv
import uuid
import os
import sys


def start():
    client = storage.Client()
    clientds = datastore.Client()

    # Create bucket
    # Bucket name must be unique
    bucket_name = 'cs1699-{}'.format(uuid.uuid4())
    print('Creating new bucket with name: {}'.format(bucket_name))
    bucket = client.create_bucket(bucket_name)
    key = clientds.key('Key')

    with open('../Big3CloudProviders.csv', 'r') as csvfile:
        csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
        for item in csvf:

            # Upload blob
            object_key = item[4].lstrip()
            blob = bucket.blob(item[4].lstrip())
            data = open("../logos/"+object_key, 'rb')
            blob.upload_from_file(data)
            blob.make_public()

            # Create URL
            url = "https://storage.googleapis.com/" + bucket_name + "/" + object_key

            # Create Entity that will pass to datastore
            entity = datastore.Entity(key=key)
            entity['provider'] = item[0]
            entity['key'] = item[1]
            entity['year'] = item[2]
            entity['logoSize'] = item[3]
            entity['url'] = url

            print(entity.values())
            clientds.put(entity)

    # Upload data and wait until input to delete
    sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                     "application will exit.")
    sys.stdout.flush()
    input()

    bucket.delete(bucket_name)


if __name__ == '__main__':
    start()
