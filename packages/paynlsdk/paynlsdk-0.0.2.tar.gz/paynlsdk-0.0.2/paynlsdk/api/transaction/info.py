import json

from marshmallow import Schema, fields, post_load, pre_load

from paynlsdk.api.requestbase import RequestBase
from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.objects import ErrorSchema, ConnectionSchema, EndUserSchema, PaymentDetailsSchema, \
    StornoDetailsSchema, SalesDataSchema, StatsDetailsSchema
from paynlsdk.validators import ParamValidator


class Request(RequestBase):
    def __init__(self, transaction_id: str=None, entrance_code: str=None):
        self.transaction_id = transaction_id
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
        return 'info'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Validation
        ParamValidator.assert_not_empty(self.transaction_id, 'transaction_id')
        # Get default api parameters
        dict = self.get_std_parameters()
        # Add own parameters
        dict['transactionId'] = self.transaction_id
        if ParamValidator.not_empty(self.entrance_code):
            dict['entranceCode'] = self.entrance_code
        return dict

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        dict = json.loads(self.raw_response)
        schema = ResponseSchema(partial=True)
        self._response, errors = schema.load(dict)
        self.handle_schema_errors(errors)


class Response(ResponseBase):
    def __init__(self,
                 connection=None,
                 enduser=None,
                 sale_data=None,
                 payment_details=None,
                 storno_details=None,
                 stats_details=None,
                 *args, **kwargs):
        self.connection = connection
        self.enduser = enduser
        self.sale_data = sale_data
        self.payment_details = payment_details
        self.storno_details = storno_details
        self.stats_details = stats_details
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.__dict__)


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema, required=True)
    connection = fields.Nested(ConnectionSchema, required=True)
    enduser = fields.Nested(EndUserSchema, required=True)
    sale_data = fields.Nested(SalesDataSchema, required=False, load_from='saleData')
    payment_details = fields.Nested(PaymentDetailsSchema, required=True, load_from='paymentDetails')
    storno_details = fields.Nested(StornoDetailsSchema, required=False, load_from='stornoDetails')
    stats_details = fields.Nested(StatsDetailsSchema, required=False, load_from='statsDetails')

    @pre_load
    def pre_processor(self, data):
        # No-op yet (see complex subtypes)
        return data

    @post_load
    def create_response(self, data):
        return Response(**data)

