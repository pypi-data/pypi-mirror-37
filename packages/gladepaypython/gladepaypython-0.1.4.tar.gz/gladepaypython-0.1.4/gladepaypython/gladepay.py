from gladepaypython.baseapi import BaseAPI
from gladepaypython.utils import *

"""docstring for Gladepay"""
class Gladepay(BaseAPI):

    def initiate_transaction(self, request):
        request_data = {
            'user': request['user'],
            'card': request['card'],
            'amount': request['amount'],
            'currency': request['currency'],
            'country': request['country'],
            'action': 'initiate',
            'paymentType': 'card'
        }

        result = self._handle_put_request('payment', request_data)
        return result

    def charge_card(self, txn_ref, auth_type, request={}):
        request_data = {
            'action': 'charge',
            'paymentType': 'card',
            'user': request['user'],
            'card': request['card'],
            'amount': request['amount'],
            'country': request['country'],
            'currency': request['currency'],
            'txnRef': txn_ref,
            'auth_type': auth_type
        }
        result = self._handle_put_request('payment', request_data)
        return result

    def charge_with_token(self, token, amount, user_details = {}):
        request_data = {
            'action': 'charge',
            'paymentType': 'token',
            'token': token,
            'user': user_details,
            'amount': amount
        }
        
        token_response = self._handle_put_request('payment', request_data)

        if 'status' in token_response:
            if token_response['status'] == 200:
                response = {
                    'status': 200,
                    'txnRef': token_response['txnRef'],
                    'message': 'Successful Payment'
                }
            else:
                response = {
                    'status': 500,
                    'message': 'Error Processing'
                }
        else:
            response = {
                'status': 500,
                'message': 'Unrecognized Response from Gateway.'
            }
        
        return response

    def account_payment(self, user_details, amount, account_details = {}):
        request_data = {
            'action': 'charge',
            'paymentType': 'account',
            'user': user_details,
            'account': account_details,
            'amount': amount
        }

        response = self._handle_put_request('payment', request_data)
        return response


    def all_banks(self):
        request_data = {
            'inquire': 'banks'
        }
        response = self._handle_put_request('resources', request_data)
        return response


    def supported_banks_account_payment(self):
        request_data = {
            'inquire': 'supported_chargable_banks'
        }
        response = self._handle_put_request('resources', request_data)
        return response

    def card_details(self, card_number):
        request_data = {
            'inquire': 'card',
            'card_no': card_number
        }
        response = self._handle_put_request('resources', request_data)
        return response

    def card_charges(self, card_no, amount):
        request_data = {
          'inquire': 'charges',
          'card_no': card_no,
          'amount': amount
        }
        response = self._handle_put_request('resources', request_data)
        return response

    def account_charges(self, amount):
        request_data = {
            'inquire': 'charges',
            'type': 'account',
            'amount': amount
        }
        response = self._handle_put_request('resources', request_data)
        return response
    

    def validate_otp(self, txn_ref, otp):
        request_data = {
            'action': 'validate',
            'txnRef': txn_ref,
            'otp': otp
        }
        result = self._handle_put_request('payment', request_data)
        return result

    def verify_transaction(self, txn_ref):
        request_data = {
            'action': 'verify',
            'txnRef': txn_ref
        }
        result = self._handle_put_request('payment', request_data)
        return result

    def money_transfer(self, amount, bankcode, account_number, sender_name, narration):
        request_data = {
            'action': 'transfer',
            'amount': amount,
            'bankcode': bankcode,
            'accountnumber': account_number,
            'sender_name': sender_name,
            'narration': narration
        }
        response = self._handle_put_request('disburse', request_data)
        return response

    def verify_money_transfer(self, txn_ref):
        request_data = {
            'action': 'verify',
            'txnRef': txn_ref
        }
        response = self._handle_put_request('disburse', request_data)
        return response

    def verify_account_name(self, bankcode, account_number):
        request_data = {
            'action': 'accountname',
            'bankcode': bankcode,
            'accountnumber': account_number
        }
        response = self._handle_put_request('resources', request_data)
        return response

    def card_payment(self, amount, country, currency, user_details, card_details):
        requests = {
            'user': user_details,
            'card': card_details,
            'amount': amount,
            'country': country,
            'currency': currency
        }
        initiate_transaction_response = self.initiate_transaction(requests)
        self.print_val("CONTENT OF I-T-Response")
        self.print_val(initiate_transaction_response)
        
        if 'status' in initiate_transaction_response:
            if initiate_transaction_response['status'] == 202:
                self.print_val("CHARGE CARD RESPONSE-184-INITIATE_TRANSACTION: ")
                self.print_val(initiate_transaction_response)
                self.print_val(type(initiate_transaction_response))
                charge_card_response = self.charge_card(initiate_transaction_response['txnRef'],
                      initiate_transaction_response['apply_auth'], requests)
                self.print_val("CHARGE CARD RESPONSE-184-Content: ")
                self.print_val(charge_card_response)

                if 'validate' in charge_card_response:
                    respond_ar = {
                        'status': 202,
                        'txnRef': charge_card_response['txnRef'],
                        'message': 'Please require the user to enter an OTP and call `validateOTP` with the `txnRef`'
                        }
                    return respond_ar
                elif 'authURL' in charge_card_response:
                    respond_ar = {
                        'status': 202,
                        'txnRef': charge_card_response['txnRef'],
                        'authURL': charge_card_response['authURL'],
                        'message': 'Please load the link contained in `authURL` for the user to validate Payment'
                    }
                    return respond_ar.to_json
                else:
                    respond_ar = {
                        'status': 500,
                        'message': 'Unrecognized Response from Gateway.'
                    }
                    return respond_ar
            else:
                response = {'status': 500, 'message': initiate_transaction_response['message']}
                return response
        else:
            response = {'status': 500, 'message': 'Unrecognized Response from Gateway.'}
            return response

    def print_val(self, param):
        # print(param)
        pass