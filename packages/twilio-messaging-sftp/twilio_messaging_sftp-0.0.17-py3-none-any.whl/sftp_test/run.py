from sftp_parse.parseCsv import ParseCsv
from sftp_parse.parseCsv import CsvContent
from sftp_client.httpClient import MessageClient
from sftp_client.s3Client import S3Client

twilioClient = MessageClient('AC1234','25ae')
csv_content = CsvContent()
content = csv_content.get_content()
parse = ParseCsv(content)
params = parse.parse()
resp = twilioClient.enqueue_messages(params,"output.csv")
print(resp)

# following needs to have valid credentials in ~/.aws/credentials or will throw exception
# s3Client = S3Client()
# s3Client.upload("test-bucket","response.csv",resp)