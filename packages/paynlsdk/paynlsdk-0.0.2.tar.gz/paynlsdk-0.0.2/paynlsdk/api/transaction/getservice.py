import json

from marshmallow import Schema, fields, post_load, pre_load

from paynlsdk.api.requestbase import RequestBase
from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.objects import ErrorSchema, MerchantSchema, ServiceSchema, CountryOptionSchema
from paynlsdk.validators import ParamValidator


class Request(RequestBase):
    def __init__(self, payment_method_id: int=None):
        self.payment_method_id = payment_method_id
        super().__init__()

    def requires_api_token(self):
        return True

    def requires_service_id(self):
        return True

    def get_version(self):
        return 12

    def get_controller(self):
        return 'Transaction'

    def get_method(self):
        return 'getService'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Get default api parameters
        dict = self.get_std_parameters()
        # Add payment_method_id if set
        if ParamValidator.not_empty(self.payment_method_id):
            dict['paymentMethodId'] = self.payment_method_id
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
                 merchant: None,
                 service: None,
                 settings: dict={},
                 country_options: dict={},
                 *args, **kwargs):
        self.merchant = merchant
        self.service = service
        self.settings = settings
        self.country_options = country_options
        super().__init__(**kwargs)

    def __repr__(self):
        return self.__dict__.__str__()


class ResponseSchema(Schema):
    request = fields.Nested(ErrorSchema, required=True)
    merchant = fields.Nested(MerchantSchema, required=True)
    service = fields.Nested(ServiceSchema, required=True)
    settings = fields.Dict(allow_none=True, required=False)
    country_options = fields.List(fields.Nested(CountryOptionSchema), allow_none=True, required=False, load_from='countryOptionList')

    @pre_load
    def preprocess(self, data):
        # Fix EMPTY settings
        if ParamValidator.is_empty(data['settings']):
            del data['settings']
        if ParamValidator.is_empty(data['countryOptionList']):
            del data['countryOptionList']
        elif 'countryOptionList' in data and ParamValidator.not_empty(data['countryOptionList']):
            #  v2.x has NO fields.Dict implementation like fields.List, so we'll have to handle this ourselves
            list = []
            for i, item in data['countryOptionList'].items():
                list.append(item)
            data['countryOptionList'] = list
        return data

    @post_load
    def create_response(self, data):
        #  This is NASTY. Perform conversion due to fields.Dict NOT taking nesteds in 2.x (aka undo preprocessing).
        #  This should be fixed in 3.x but that's a pre-release
        if 'country_options' in data:
            dict = {}
            for item in data['country_options']:
                dict[item.id] = item
            data['country_options'] = dict
        return Response(**data)

