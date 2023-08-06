import json

from paynlsdk.api.requestbase import RequestBase
from paynlsdk.api.responsebase import ResponseBase
from paynlsdk.objects import Error, BankDetailsSchema


class Request(RequestBase):
    def __init__(self):
        super().__init__()

    def requires_api_token(self):
        return False

    def requires_service_id(self):
        return False

    def get_version(self):
        return 12

    def get_controller(self):
        return 'Transaction'

    def get_method(self):
        return 'getBanks'

    def get_query_string(self):
        return ''

    def get_parameters(self):
        # Get default api parameters
        dict = self.get_std_parameters()
        # No further parameters
        return dict

    @RequestBase.raw_response.setter
    def raw_response(self, raw_response):
        self._raw_response = raw_response
        # Do error checking.
        dict = json.loads(self.raw_response)
        # The raw result IS a list, so we need the "many=True" argument
        schema = BankDetailsSchema(partial=True, many=True)
        # Bit of an oddball here. Result is a pure array of banks, so we'll mimic a decent response
        banks, errors = schema.load(dict)
        self.handle_schema_errors(errors)
        kwargs = {"result": Error(result=True), "banks": banks}
        self._response = Response(**kwargs)

    def __repr__(self):
        return self.__dict__.__str__()


class Response(ResponseBase):
    def __init__(self,
                 banks: list=[],
                 *args, **kwargs):
        self.banks = banks
        # the result is a list. We'll mimic the request object IF not yet available (should have been done though)
        if 'request' not in kwargs:
            kwargs['request'] = Error(result=True)
        super().__init__(**kwargs)

    def __repr__(self):
        return self.__dict__.__str__()

