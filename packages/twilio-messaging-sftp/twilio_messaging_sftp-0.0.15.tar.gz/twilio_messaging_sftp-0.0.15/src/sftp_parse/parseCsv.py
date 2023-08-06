import csv
import os
from sftp_parse.parseError import ParseError
from sftp_parse.queryParams import QueryParams


class CsvContent(object):
    # used for now until we pass it an s3 location
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fileName = os.path.join(fileDir, '../sftp_test/data.csv')
    path = ''

    def __init__(self, path=fileName):
        self.path = path

    def get_content(self):
        return open(self.path).read()


class ParseCsv(object):
    content = ''

    def __init__(self, content):
        self.content = content

    def parse(self):
        sniffer = csv.Sniffer()

        # for now we are keeping the header to be in the format of lower case and underscore for two words
        # for example, to, from, body, media_url
        if sniffer.has_header(self.content) is True:
            # verify there is a header
            reader = csv.DictReader(self.content.splitlines(), skipinitialspace=True)
            if 'to' not in reader.fieldnames:
                return ParseError(500, "Missing the to field!")

            if 'from' not in reader.fieldnames:
                return ParseError(500, "Missing the from field!")

            if 'body' not in reader.fieldnames:
                return ParseError(500, "Missing the body field!")

            queries = []
            for row in reader:
                to = row['to']
                from_ = row['from']
                body = row['body']

                if (to is None or to is "") or (from_ is None or from_ is "") or (body is None or body is ""):
                    return ParseError(500, "No values for fields required for sending a message")
                else:
                    media_url = None
                    if ('media_url' in reader.fieldnames) and (row['media_url'] is not ""):
                        media_url = row['media_url']

                    queries.append(QueryParams(to, from_, body, media_url, row))
            return queries
