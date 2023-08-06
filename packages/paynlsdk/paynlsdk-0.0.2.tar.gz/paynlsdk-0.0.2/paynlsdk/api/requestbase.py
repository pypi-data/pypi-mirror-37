import json
from urllib.parse import urlencode
from abc import ABC, abstractmethod

from marshmallow import Schema, fields, post_load

from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.exceptions import SchemaException
from paynlsdk.objects import ErrorSchema
from paynlsdk.validators import ParamValidator


class RequestBase(ABC):
    def __init__(self):
        self._api_token = None
        self._service_id = None
        self._raw_response = None
        self._response = None

    @property
    def api_token(self):
        return self._api_token

    @api_token.setter
    def api_token(self, api_token: str):
        self._api_token = api_token

    @property
    def service_id(self):
        return self._service_id

    @service_id.setter
    def service_id(self, service_id: str):
        self._service_id = service_id

    @property
    def raw_response(self):
        return self._raw_response

    @raw_response.setter
    def raw_response(self, raw_response: str):
        self._raw_response = raw_response

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: str):
        self._response = response

    @abstractmethod
    def requires_api_token(self):
        pass

    @abstractmethod
    def requires_service_id(self):
        pass

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def get_controller(self):
        pass

    @abstractmethod
    def get_method(self):
        pass

    @abstractmethod
    def get_query_string(self):
        pass

    def get_url(self):
        return 'v{0}/{1}/{2}/json'.format(self.get_version(), self.get_controller(), self.get_method())

    def get_std_parameters(self):
        dict = {}
        if self.requires_api_token():
            ParamValidator.assert_not_empty(self.api_token, 'api_token')
            dict["token"] = self.api_token
        if self.requires_service_id():
            ParamValidator.assert_not_empty(self.service_id, 'service_id')
            dict["serviceId"] = self.service_id
        return dict

    def to_query_string(self):
        dict = self.get_parameters()
        if dict.__len__() == 0:
            return ""
        return urlencode(dict)

    @abstractmethod
    def get_parameters(self):
        pass

    def handle_schema_errors(self, error_dict):
        if error_dict:
            raise SchemaException(error_dict)


class Test(RequestBase):
    def __init__(self):
        super().__init__()

    def requires_api_token(self):
        return True

    def requires_service_id(self):
        return True

    def get_version(self):
        return 1

    def get_controller(self):
        return 'test'

    def get_method(self):
        return 'get'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Get default api parameters
        dict = self.get_std_parameters()
        # Append other parameters
        dict['a'] = 'b'
        dict['c'] = {'x':1, 'y':2}
        return dict

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        # Do error checking.
        dict = json.loads(self.raw_response)
        if 'request' not in dict:
            raise ValueError("request result not set in response")

        if 'test' not in dict:
            raise ValueError("response data not set in response")

        schema = ErrorSchema()
        error, errors = schema.load(dict['request'])

        del dict['request']
        schema = TestResponseSchema(partial=True)
        self._response, errors = schema.load(dict)


class TestResponse(ResponseBase):
    def __init__(self, test=None, *args, **kwargs):
        self.test = test
        super().__init__(**kwargs)


class TestResponseSchema(Schema):
    test = fields.String()

    @post_load
    def create_testresponse(self, data):
        return TestResponse(**data)


class TestResponseSchema2(Schema):
    request = fields.Nested(ErrorSchema)
    test = fields.String()

    @post_load
    def create_testresponse(self, data):
        return TestResponse(**data)


# raw = "{\"request\": {\"result\": \"1\",\"errorId\": \"\",\"errorMessage\": \"\"},\"test\": \"this is a test response\"}"
# test = Test()
# test.api_token = 'apitoken982435'
# test.service_id = 'svcid8235r'
#
# print(test.api_token)
# print(test.get_url())
# print(test.get_parameters())
# print(test.to_query_string())
#
# test.raw_response = raw
# print("DONE")
# print(test.response)

# rawjson = json.loads(raw)
# schema = TestResponseSchema2()
# dict, errors = schema.load(rawjson)
#
# print('dump raw json string')
# print(raw)
# print('dump raw json object')
# print(rawjson)
# print('dump dict')
# print(dict)
# print('dump dict.__dict__')
# print(dict.__dict__)
# print('dump schema DUMPS')
# print(schema.dumps(dict))
