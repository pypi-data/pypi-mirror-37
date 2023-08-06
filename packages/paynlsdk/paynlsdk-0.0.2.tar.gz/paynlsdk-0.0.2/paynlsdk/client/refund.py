from paynlsdk.api.client import APIClient


class Refund(object):
    @staticmethod
    def info(refund_id: str):
        from paynlsdk.api.refund.info import Request
        client = APIClient()
        request = Request(refund_id)
        client.perform_request(request)
        return request.response

    @staticmethod
    def transaction(transaction_id: str,
                    amount: int=None,
                    description: str=None,
                    process_date: str=None,
                    products: dict={},
                    vat_percentage: float=None,
                    exchange_url: str=None):
        from paynlsdk.api.refund.transaction import Request
        client = APIClient()
        request = Request(transaction_id, amount, description, process_date, products, vat_percentage, exchange_url)
        client.perform_request(request)
        return request.response

    @staticmethod
    def info_request():
        from paynlsdk.api.refund.info import Request
        return Request()

    @staticmethod
    def transaction_request():
        from paynlsdk.api.refund.info import Request
        return Request()
