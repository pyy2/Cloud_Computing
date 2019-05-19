import os
import uuid
import sys
import csv
import time
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

try:
    # Create the BlockBlockService that is used to call the Blob service for the storage account
    block_blob_service = BlockBlobService(account_name='account_name',
                                          account_key='account_key')

    container_name = 'cs1699-{}'.format(uuid.uuid4())  # Generate random name
    print('Creating new bucket with name: {}'.format(container_name))

    # Create a container with unique name and set the permission so the blobs are public.
    block_blob_service.create_container(
        container_name, public_access=PublicAccess.Container)
    print('Creating new container with name: {}'.format(container_name))

    table_service = TableService(account_name='account_name',
                                 account_key='account_key')

    if table_service.create_table('Big3CloudProviders'):
        print('Table Created!')
    else:
        print("Table already exists or another error")

    # Open csv file and read data into table
    print('Loading Data...')
    with open('../Big3CloudProviders.csv', 'r') as csvfile:
        csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
        for item in csvf:
            body = open('../Big3CloudProviders.csv', 'rb')
            object_key = item[4].lstrip()

            print('Creating blob from path...')
            block_blob_service.create_blob_from_path(
                container_name, item[4],
                '../logos/' + object_key
            )

            print('Creating URL from path...')
            # Create a url of the object
            url = "https://cs1699data.blob.core.windows.net/logos/"+object_key
            print(url)

            metadata_item = {'provider': item[0], 'key': item[1],
                             'year': item[2], 'logoSize': item[3], 'fileName': url}
            try:
                table_service.insert_entity(
                    'Big3CloudProviders', metadata_item)
            except:
                print("Item may already be there or another failure")

    sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                     "application will exit.")
    sys.stdout.flush()
    input()

    # Clean up resources. This includes the container and the temp files
    table_service.delete_table('Big3CloudProviders')
    print('Deleted Table: Big3CloudProviders')
    block_blob_service.delete_container(container_name)
    print('Deleted container: ' + container_name)
except Exception as e:
    print(e)
