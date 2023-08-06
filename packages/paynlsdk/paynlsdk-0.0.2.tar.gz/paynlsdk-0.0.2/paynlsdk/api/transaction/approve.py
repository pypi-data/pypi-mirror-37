import json

from marshmallow import Schema, fields, post_load

from paynlsdk.api.requestbase import RequestBase
from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.objects import ErrorSchema
from paynlsdk.validators import ParamValidator


class Request(RequestBase):
    def __init__(self, order_id: str=None, entrance_code: str=None):
        self.order_id = order_id
        self.entrance_code = entrance_code
        super().__init__()

    def requires_api_token(self):
        return True

    def requires_service_id(self):
        return False

    def get_version(self):
        return 12

    def get_controller(self):
        return 'Transaction'

    def get_method(self):
        return 'approve'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Validation
        ParamValidator.assert_not_empty(self.transaction_id, 'transaction_id')
        # Get default api parameters
        dict = self.get_std_parameters()
        # Add own parameters
        dict['orderId'] = self.order_id
        if ParamValidator.not_empty(self.entrance_code):
            dict['entranceCode'] = self.entrance_code
        return dict

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        # Do error checking.
        dict = json.loads(self.raw_response)
        schema = ResponseSchema(partial=True)
        self._response, errors = schema.load(dict)
        self.handle_schema_errors(errors)


class Response(ResponseBase):
    def __init__(self,
                 message: str=None,
                 *args, **kwargs):
        self.message = message
        super().__init__(**kwargs)


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema)
    message = fields.String(required=False)

    @post_load
    def create_response(self, data):
        return Response(**data)

