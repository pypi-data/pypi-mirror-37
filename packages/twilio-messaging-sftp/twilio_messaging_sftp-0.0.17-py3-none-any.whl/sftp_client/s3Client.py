import logging
import boto3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class S3Client:
    """A wrapper client for interacting with Amazon S3"""

    def __init__(self, access_key, secret_key):
        """Initialize s3 client """
        self.s3 = boto3.resource('s3')

    def print_buckets(self):
        response = self.s3.list_buckets()
        # Get a list of all bucket names from the response
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        # Print out the bucket list
        print("Bucket List: %s" % buckets)

    def uploadString(self, bucket, key, data):
        self.s3.put_object(Body=data, Bucket=bucket, Key=key)

    def uploadFile(self, bucket, key, filename):
        self.s3.upload_file(Filename=filename,Bucket=bucket, Key=key)



