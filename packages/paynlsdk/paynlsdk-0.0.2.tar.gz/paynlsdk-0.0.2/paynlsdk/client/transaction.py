from paynlsdk.api.client import APIClient
from paynlsdk.objects import TransactionData, TransactionStartStatsData, SalesData, TransactionEndUser


class Transaction(object):
    @staticmethod
    def approve(order_id: str, entrance_code: str=None):
        from paynlsdk.api.transaction.approve import Request
        client = APIClient()
        request = Request(order_id, entrance_code)
        client.perform_request(request)
        return request.response

    @staticmethod
    def decline(order_id: str, entrance_code: str=None):
        from paynlsdk.api.transaction.decline import Request
        client = APIClient()
        request = Request(order_id, entrance_code)
        client.perform_request(request)
        return request.response

    @staticmethod
    def capture(transaction_id: str, products: dict={}, tracktrace: str=None):
        from paynlsdk.api.transaction.capture import Request
        client = APIClient()
        request = Request(transaction_id, products, tracktrace)
        client.perform_request(request)
        return request.response

    @staticmethod
    def get_banks():
        from paynlsdk.api.transaction.getbanks import Request
        client = APIClient()
        request = Request()
        client.perform_request(request)
        return request.response

    @staticmethod
    def get_service(payment_method_id: int):
        from paynlsdk.api.transaction.getservice import Request
        client = APIClient()
        request = Request(payment_method_id)
        client.perform_request(request)
        return request.response

    @staticmethod
    def info(transaction_id: str, entrance_code: str=None):
        from paynlsdk.api.transaction.info import Request
        client = APIClient()
        request = Request(transaction_id, entrance_code)
        client.perform_request(request)
        return request.response

    @staticmethod
    def status(transaction_id: str):
        from paynlsdk.api.transaction.status import Request
        client = APIClient()
        request = Request(transaction_id)
        client.perform_request(request)
        return request.response

    @staticmethod
    def start(amount: str,
              ip_address: str,
              finish_url: str,
              payment_option_id: int=None,
              payment_option_sub_id: int=None,
              transaction: TransactionData=None,
              stats_data: TransactionStartStatsData=None,
              end_user: TransactionEndUser=None,
              sale_data: SalesData=None,
              test_mode: bool=False,
              transfer_type: str=None,
              transfer_value: str=None
              ):
        from paynlsdk.api.transaction.start import Request
        client = APIClient()
        request = Request(amount, ip_address, finish_url, payment_option_id, payment_option_sub_id,
                          transaction, stats_data, end_user, sale_data, test_mode, transfer_type, transfer_value)
        client.perform_request(request)
        return request.response

    @staticmethod
    def approve_request():
        from paynlsdk.api.transaction.approve import Request
        return Request()

    @staticmethod
    def decline_request():
        from paynlsdk.api.transaction.decline import Request
        return Request()

    @staticmethod
    def capture_request():
        from paynlsdk.api.transaction.capture import Request
        return Request()

    @staticmethod
    def get_banks_request():
        from paynlsdk.api.transaction.getbanks import Request
        return Request()

    @staticmethod
    def get_service_request():
        from paynlsdk.api.transaction.getservice import Request
        return Request()

    @staticmethod
    def info_request():
        from paynlsdk.api.transaction.info import Request
        return Request()

    @staticmethod
    def status_request():
        from paynlsdk.api.transaction.status import Request
        return Request()

    @staticmethod
    def start_request():
        from paynlsdk.api.transaction.start import Request
        return Request()

# print(Transaction.get_banks())