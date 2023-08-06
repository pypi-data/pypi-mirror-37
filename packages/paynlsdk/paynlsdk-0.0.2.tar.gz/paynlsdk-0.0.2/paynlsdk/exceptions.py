
class ErrorException(Exception):
  def __init__(self, error):
    self.error = error
    message = error.message
    super(ErrorException, self).__init__(message)


class SchemaException(Exception):
  def __init__(self, error_dict):
    self.errors = error_dict
    message = '\n'.join(['{}: {}'.format(str(k), ', '.join(str(e) for e in v)) for k, v in self.errors.items()])
    super(SchemaException, self).__init__(message)

