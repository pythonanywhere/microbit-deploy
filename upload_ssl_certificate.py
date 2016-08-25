#!/usr/bin/env python
"""Upload the PythonAnywhere HTTPS cert to Amazon

Usage:
   upload_ssl_certificate.py --aws_access_key=<access_key> --aws_secret_key=<secret_key>
                            --certificate=<certificate_file>  --chain=<chain-file>
                            --private_key=<private_key_file>

"""


from boto.iam.connection import IAMConnection
from datetime import datetime
from docopt import docopt


def main():
    arguments = docopt(__doc__)
    aws_access_key = arguments["--aws_access_key"]
    aws_secret_key = arguments["--aws_secret_key"]
    with open(arguments["--certificate"], "r") as f:
        certificate = f.read()
    with open(arguments["--chain"], "r") as f:
        chain = f.read()
    with open(arguments["--private_key"], "r") as f:
        private_key = f.read()

    connection = IAMConnection(aws_access_key, aws_secret_key)
    connection.upload_server_cert(
        "PythonAnywhere-main-wildcard-cert-{:%Y-%m-%d}".format(datetime.now()),
        certificate,
        private_key,
        chain,
        path="/cloudfront/",
    )



if __name__ == "__main__":
    main()
