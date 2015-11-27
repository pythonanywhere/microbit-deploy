#!/usr/bin/env python
"""Create a new CloudFront distribution for a Python Microbit editor deploy

Usage:
   create_distribution.py --aws_access_key=<access_key> --aws_secret_key=<secret_key>
                          --s3_bucket_name=<s3_bucket_name> --ssl_cert_id=<ssl_cert_id> <domain>

"""

from boto.cloudfront import CloudFrontConnection
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from docopt import docopt
import os
from textwrap import dedent


def create_s3_bucket(aws_access_key, aws_secret_key, s3_bucket_name):
    connection = S3Connection(aws_access_key, aws_secret_key)

    bucket = connection.create_bucket(s3_bucket_name, location='eu-west-1')
    bucket.configure_website(suffix="index.html")

    policy = dedent("""
        {{
          "Version": "2012-10-17",
          "Statement": [
            {{
              "Sid": "PublicReadGetObject",
              "Effect": "Allow",
              "Principal": {{
                "AWS": "*"
              }},
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::{s3_bucket_name}/*"
            }}
          ]
        }}
    """).format(s3_bucket_name=s3_bucket_name).strip()
    bucket.set_policy(policy)


    index_file_key = Key(bucket)
    index_file_key.key = "index.html"
    default_index_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "default_index.html")
    index_file_key.set_contents_from_filename(default_index_file)

    return bucket.get_website_endpoint()



def create_cloudfront_distribution(aws_access_key, aws_secret_key, bucket_endpoint, ssl_cert_id, domain):
    connection = CloudFrontConnection(aws_access_key, aws_secret_key)
    connection
    print bucket_endpoint



def main():
    arguments = docopt(__doc__)
    aws_access_key = arguments["--aws_access_key"]
    aws_secret_key = arguments["--aws_secret_key"]
    s3_bucket_name = arguments["--s3_bucket_name"]
    ssl_cert_id = arguments["--ssl_cert_id"]
    domain = arguments["<domain>"]

    bucket_endpoint = create_s3_bucket(aws_access_key, aws_secret_key, s3_bucket_name)
    create_cloudfront_distribution(
        aws_access_key, aws_secret_key,
        bucket_endpoint, ssl_cert_id, domain
    )






if __name__ == "__main__":
    main()
