import hashlib
import inspect
import logging
import requests

from enum import IntEnum
from requests.exceptions import RequestException
from delorean import Delorean
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt
from .errors import ClientError, TryAgain


logger = logging.getLogger(__name__)


class PlatformError(IntEnum):
    APP_CALL_LIMITED = 7
    REMOTE_SERVICE_ERROR = 15


class Client:
    def __init__(self, app_id, app_secret, service_url):
        self.app_id = app_id
        self.app_secret = app_secret
        self.service_url = service_url

    @retry(retry=retry_if_exception_type((TryAgain, RequestException)), wait=wait_exponential(max=600), stop=stop_after_attempt(20), reraise=True)
    def call(self, method, params=None, token=None, timeout=8):
        if params is None:
            params = {}

        _params = {
            'app_key': self.app_id,
            'format': 'json',
            'method': method,
            'sign_method': 'md5',
            'timestamp': Delorean(timezone='Asia/Shanghai').datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'v': 2.0
        }
        payload = {**_params, **params}
        
        if token is not None:
            payload['session'] = token

        payload['sign'] = Client.sign(payload, self.app_secret)

        response = requests.post(self.service_url, data=payload, timeout=timeout)
        output = response.json()

        logger.info('{} {}\n    Payload: {}\n    Output: {}'.format(method, response, payload, output))

        response.raise_for_status()
        Client.raise_for_error(data=output)

        return output

    @staticmethod
    def sign(data, secret):
        source = secret + ''.join([key+str(data[key]) for key in sorted(data.keys())]) + secret
        return hashlib.md5(source.encode()).hexdigest().upper()

    @staticmethod
    def raise_for_error(data):
        """
        Ref: http://open.taobao.com/doc.htm?docId=101645&docType=1
        """
        error = data.get('error_response')
        if not error:
            return

        try:
            if error['code'] == PlatformError.APP_CALL_LIMITED:
                raise TryAgain(error)
            elif error['code'] == PlatformError.REMOTE_SERVICE_ERROR and error['sub_code'].startswith('isp.'):
                raise TryAgain(error)
            else:
                raise ClientError(error)
        except (KeyError, AttributeError):
            raise ClientError(error)
