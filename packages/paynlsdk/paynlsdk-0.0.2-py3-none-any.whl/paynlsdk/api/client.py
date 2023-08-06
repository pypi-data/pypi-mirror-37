import json
import sys
import requests
from paynlsdk.api.requestbase import RequestBase
from paynlsdk.exceptions import ErrorException
from paynlsdk.validators import ParamValidator

PAYNL_END_POINT = "https://rest-api.pay.nl"
PAYNL_CLIENT_VERSION = "0.0.1"


class APIAuthentication(object):
    api_token = None
    service_id = None


class APIClient(object):
    print_debug = False

    def __init__(self):
        self.__supported_status_codes = [200]
        self.end_point = PAYNL_END_POINT
        self.client_version = PAYNL_CLIENT_VERSION
        self.api_token = None
        self.service_id = None

    def user_agent(self):
        version = '{0}.{1}.{2}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
        return "PAYNL/SDK/{0} Python/{1} ({2})".format(self.client_version, version, sys.hexversion)

    def perform_request(self,
                        request: RequestBase,
                        method: str='POST'
                        ):
        headers = {
          'Accept': 'application/json',
          'User-Agent': self.user_agent()
        }

        # Lazy loader for api credentials.
        if request.requires_api_token() and ParamValidator.is_empty(request.api_token)\
                and ParamValidator.not_empty(APIAuthentication.api_token):
            request.api_token = APIAuthentication.api_token
        if request.requires_service_id() and ParamValidator.is_empty(request.service_id)\
                and ParamValidator.not_empty(APIAuthentication.service_id):
                request.service_id = APIAuthentication.service_id

        # Build url
        url = "{0}/{1}".format(PAYNL_END_POINT, request.get_url())

        if self.print_debug:
            print("Calling {} using {}".format(url, method))
            print("Params: {}".format(json.dumps(request.get_parameters())))

        if method.upper() == 'GET':
            response = requests.get(url, verify=True, headers=headers, params=request.get_parameters())
        else:
            response = requests.post(url, verify=True, headers=headers, data=request.get_parameters())

        if response.status_code not in self.__supported_status_codes:
            response.raise_for_status()

        if self.print_debug:
            print("Response object: {}".format(response))
            print("Raw response: {}".format(response.text))

        # Now the we have a response, let the request class handle the response.
        request.raw_response = response.text

        if self.print_debug:
            print(type(request.response))

        if request.response.is_error():
            raise ErrorException(request.response.request)
