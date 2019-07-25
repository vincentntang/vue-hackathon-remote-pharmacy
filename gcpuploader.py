from google.cloud import storage
import os
import sys


def uploadtobucket(filename, bucketname):
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    ##storage_client = storage.Client.from_service_account_json('googlecreds.json')
    storage_client = storage.Client.from_service_account_json('gc.json')

    # Make an authenticated API request
##    buckets = list(storage_client.list_buckets())
##    print(buckets)

    bucket = storage_client.get_bucket(bucketname)

    destination_blob_name = filename
    source_file_name = filename

    blob = bucket.blob(destination_blob_name)
    
    blob.cache_control = "no-cache"
    blob.upload_from_filename(source_file_name)
    ##blob.make_public()
    blob.cache_control = "no-cache"

    print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))



filename = sys.argv[1]
bucketname = sys.argv[2]

uploadtobucket(filename, bucketname)
