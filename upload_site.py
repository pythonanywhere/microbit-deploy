#!/usr/bin/env python
"""Upload a Microbit distribution to an S3 bucket that is already being hosted on CloudFront

Usage:
   upload_site.py --aws_access_key=<access_key> --aws_secret_key=<secret_key>
                  --s3_bucket_name=<s3_bucket_name> --cloudfront_distribution=<cloudfront_distribution> <path>

"""

from boto.cloudfront import CloudFrontConnection
from boto.s3 import connect_to_region
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from docopt import docopt
import os


def upload_to_s3_bucket(aws_access_key, aws_secret_key, s3_bucket_name, path):
    s3_connection = S3Connection(aws_access_key, aws_secret_key)

    bucket = s3_connection.get_bucket(s3_bucket_name)

    # Workaround for boto issue #2207 as per anna-buttfield-sirca
    # at https://github.com/boto/boto/issues/2207#issuecomment-60682869
    bucket_location = bucket.get_location()
    if bucket_location:
        s3_connection = connect_to_region(
            bucket_location,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        bucket = s3_connection.get_bucket(s3_bucket_name)

    print("Deleting existing content")
    for key in bucket.list():
        key.delete()

    print("Uploading new content")
    for (source_path, directories, files) in os.walk(path):
        assert source_path.startswith(path)
        dest_path = source_path[len(path):]
        for filename in files:
            if filename == ".gitignore":
                print "Skipping .gitignore"
                continue
            print "Uploading {} from {} to {}".format(filename, source_path, dest_path)
            if dest_path.startswith(".git"):
                print "It's in a .git* directory, skipping"
                continue
            key = Key(bucket)
            key.key = os.path.join(dest_path, filename)
            key.set_contents_from_filename(os.path.join(source_path, filename))



def invalidate_all(aws_access_key, aws_secret_key, cloudfront_distribution):
    print("Invalidating all")
    cloudfront_connection = CloudFrontConnection(aws_access_key, aws_secret_key)
    cloudfront_connection.create_invalidation_request(cloudfront_distribution, "/*")



def main():
    arguments = docopt(__doc__)
    aws_access_key = arguments["--aws_access_key"]
    aws_secret_key = arguments["--aws_secret_key"]
    s3_bucket_name = arguments["--s3_bucket_name"]
    cloudfront_distribution = arguments["--cloudfront_distribution"]
    path = arguments["<path>"]
    if not path.endswith("/"):
        path += "/"

    upload_to_s3_bucket(aws_access_key, aws_secret_key, s3_bucket_name, path)
    invalidate_all(aws_access_key, aws_secret_key, cloudfront_distribution)


if __name__ == "__main__":
    main()
