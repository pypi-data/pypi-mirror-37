class QueryParams(object):
    to = ""
    from_ = ""
    body = ""
    media_url = ""
    all_params = []

    def __init__(self, to, from_, body, media_url, all_params):
        self.to = to
        self.from_ = from_
        self.body = body
        self.media_url = media_url
        self.all_params = all_params

    def __repr__(self):
        return "to: {0}, from: {1}, body: {2}, media_url: {3}, all_params: {4}".format(self.to, self.from_, self.body, self.media_url, self.all_params)
