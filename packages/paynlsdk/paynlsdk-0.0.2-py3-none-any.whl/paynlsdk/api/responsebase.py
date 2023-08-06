
class ResponseBase(object):

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        return

    def is_error(self):
        return self.request is not None and not self.request.result

