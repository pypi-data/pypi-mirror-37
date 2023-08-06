from src import ParseCsv
from src.client import MessageClient

client = MessageClient('AC01234','1234')
parse = ParseCsv()
params = parse.parse()
client.enqueue_messages(params)
