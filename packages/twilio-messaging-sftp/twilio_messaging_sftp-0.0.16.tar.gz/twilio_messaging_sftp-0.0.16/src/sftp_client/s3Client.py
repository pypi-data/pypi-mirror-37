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

    def upload(self, bucket, key, data):
        self.s3.put_object(Bucket=bucket, Key=key, Body=data)



