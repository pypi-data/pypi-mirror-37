import json

from marshmallow import Schema, fields, post_load

from paynlsdk.api.requestbase import RequestBase
from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.objects import Error
from paynlsdk.validators import ParamValidator


class Request(RequestBase):
    def __init__(self, ip_address: str=None):
        self.ip_address = ip_address
        super().__init__()

    def requires_api_token(self):
        return False

    def requires_service_id(self):
        return False

    def get_version(self):
        return 1

    def get_controller(self):
        return 'Validate'

    def get_method(self):
        return 'isPayServerIp'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Validation
        ParamValidator.assert_not_empty(self.ip_address, 'ip_address')
        # Get default api parameters
        dict = self.get_std_parameters()
        # Add own parameters
        dict['ipAddress'] = self.ip_address
        return dict

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        # Do error checking.
        dict = json.loads(self.raw_response)
        schema = ResponseSchema(partial=True)
        self._response, errors = schema.load(dict)
        self.handle_schema_errors(errors)

    def __repr__(self):
        return self.__dict__.__str__()


class Response(ResponseBase):
    def __init__(self,
                 result: bool=None,
                 *args, **kwargs):
        self.result = result
        # the result is a pure boolean, so we'll mimic the base's request object
        kwargs['request'] = Error(result=result)
        super().__init__(**kwargs)

    def __repr__(self):
        return self.__dict__.__str__()


class ResponseSchema(Schema):
    result = fields.Boolean()

    @post_load
    def create_response(self, data):
        return Response(**data)

