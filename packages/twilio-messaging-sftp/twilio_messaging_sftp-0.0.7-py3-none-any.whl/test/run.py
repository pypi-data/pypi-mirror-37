from parse.parseCsv import ParseCsv
from client.httpClient import MessageClient

client = MessageClient('AC01234','1234')
parse = ParseCsv()
params = parse.parse()
client.enqueue_messages(params)
