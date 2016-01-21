# microbit-deploy

This repository contains helpers designed to deploy the BBC Micro:bit Python Editor for the TouchDevelop IDE, via its hosting provider, PythonAnywhere, and Amazon AWS cloudfront + S3.

The main command is *upload_site.py*.  Try

```
  ./upload_site.py --help
```
  
For more info.  The key things you'll need are

* a checkout of the microbit python editor source files
* an AWS access key and secret with appropriate IAM perms to the PythonAnywhere AWS account.
