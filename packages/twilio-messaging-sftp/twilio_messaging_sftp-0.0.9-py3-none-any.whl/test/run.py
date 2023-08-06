from src.client import MessageClient
from src.parse import ParseCsv

client = MessageClient('AC01234','1234')
parse = ParseCsv()
params = parse.parse()
client.enqueue_messages(params)
