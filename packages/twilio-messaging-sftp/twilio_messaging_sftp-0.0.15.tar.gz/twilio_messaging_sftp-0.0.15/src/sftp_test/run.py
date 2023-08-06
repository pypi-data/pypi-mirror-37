from sftp_parse.parseCsv import ParseCsv
from sftp_parse.parseCsv import CsvContent
from sftp_client.httpClient import MessageClient

client = MessageClient('AC01234','1234')
csv_content = CsvContent()
content = csv_content.get_content()
parse = ParseCsv(content)
params = parse.parse()
client.enqueue_messages(params)
