import json

from marshmallow import Schema, fields, post_load

from paynlsdk.api.requestbase import RequestBase
from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.objects import ErrorSchema, RefundInfo
from paynlsdk.validators import ParamValidator


class Request(RequestBase):
    def __init__(self, refund_id: str=None):
        self.refund_id = refund_id
        super().__init__()

    def requires_api_token(self):
        return True

    def requires_service_id(self):
        return False

    def get_version(self):
        return 3

    def get_controller(self):
        return 'Refund'

    def get_method(self):
        return 'info'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Validation
        ParamValidator.assert_not_empty(self.refund_id, 'refund_id')
        # Get default api parameters
        dict = self.get_std_parameters()
        # Add own parameters
        dict['refundId'] = self.refund_id
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
                 refund=None,
                 *args, **kwargs):
        self.refund = refund
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.__dict__)


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema, required=True)
    refund = fields.Nested(RefundInfo, required=True, load_from='refund')

    @post_load
    def create_response(self, data):
        return Response(**data)


