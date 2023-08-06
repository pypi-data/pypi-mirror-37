from paynlsdk.api.client import APIClient


class Validate(object):
    @staticmethod
    def pay_server_ip(ip_address: str=None):
        from paynlsdk.api.validate.payserverip import Request
        client = APIClient()
        request = Request(ip_address)
        client.perform_request(request)
        return request.response

