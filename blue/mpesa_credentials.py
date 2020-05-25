import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'YfyUAwRiviYhr9JzQV7p9Fiyp3I61Wky'
    consumer_secret = 'wrxUBxwcfNRMHOPA'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    def __init__(self):
        self.r = requests.get(MpesaC2bCredential.api_URL,
                              auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
        self.mpesa_access_token = json.loads(self.r.text)
        self.validated_mpesa_access_token = self.mpesa_access_token['access_token']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None or exc_value is None or traceback is not None:
            return exc_value


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    Test_c2b_shortcode = "600589"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')


class PaymentTypes:
    deposits = 1
    share_capital = 2
    loan_application = 3
    loan_payment = 4
