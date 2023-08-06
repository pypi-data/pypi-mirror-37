import os
import requests
import json
import gladepaypython.version

from gladepaypython.errors import *

class BaseAPI(object):
    """
    This is the Base class for the gladepaypython API wrapper for gladepay
    This class should not be directly instantiated.
    """
    _CONTENT_TYPE = 'application/json'
    _BASE_END_POINT_LIVE = 'https://api.gladepay.com'
    _BASE_END_POINT_TEST = 'https://demo.api.gladepay.com'
    _BASE_END_POINT = ''


    # attr_reader :merchant_id, :merchant_key, :base_url, :live
    def __init__(self, merchant_id=None, merchant_key=None, live=False):
        if merchant_id:
            self._GLADEPAY_MERCHANT_ID = merchant_id
        else:
            self._GLADEPAY_MERCHANT_ID = os.getenv('merchant_id', None)

        if not self._GLADEPAY_MERCHANT_ID:
            raise MissingAuthKeyError("Gladepay Merchant ID Is Missing At Either ID Argument Or Environment Variable")

        if merchant_key:
            self._GLADEPAY_MERCHANT_KEY = merchant_key
        else:
            self._GLADEPAY_MERCHANT_KEY = os.getenv('MERCHANT_KEY', None)

        if not self._GLADEPAY_MERCHANT_KEY:
            raise MissingAuthKeyError("Gladepay Merchant Key Is Missing At Either Key Argument or Environment Variable")
        
        if live:
            self._BASE_END_POINT = self._BASE_END_POINT_LIVE
        else:
            self._BASE_END_POINT = self._BASE_END_POINT_TEST

    def _url(self, path):
        return self._BASE_END_POINT + path

    def _headers(self):
        return {
            "Content-Type": self._CONTENT_TYPE,
            "mid": self._GLADEPAY_MERCHANT_ID,
            "key": self._GLADEPAY_MERCHANT_KEY 
        }

    '''
    This function takes in every json response sent back by the
    server and trys to get out the important return variables
    Returns a python tuple of status code, status(bool), message, data
    '''
    def _parse_json(self, response_obj):
        parsed_response = response_obj.json()
        status = parsed_response.get('status', None)
        message = parsed_response.get('message', None)
        data = parsed_response.get('data', None)

        return response_obj.status_code, status, message, data

    def _handle_put_request(self, method_call_type, data=None):
        """
        A function to handle specific type of call in this case PUT
        """
        url = self._url('/' + method_call_type)
        self.print_val("URL-LINK: ")
        self.print_val(url)
        return self._handle_request('PUT', url, data)

    def _handle_request(self, method, url, data=None):
        """
        A function to handle all API url calls
        Returns a python tuple of status code, status(bool), message, data
        """
        method_map = {
                    'PUT':requests.put,
                    'GET':requests.get,
                    'POST':requests.post,
                    'DELETE':requests.delete
                    }

        payload = json.dumps(data) if data else data
        request = method_map.get(method)
        self.print_val("PAYLOAD")
        self.print_val(payload)

        if not request:
            raise InvalidMethodError("Request method not recognised or implemented")

        response = request(url, headers=self._headers(), data=payload, verify=True)
        self.print_val("RESPONSE-BODY-No-JSON: ")
        self.print_val(response)
        self.print_val("RESPONSE-BODY-STATUS_CODE: ")
        self.print_val(response.status_code)
        self.print_val("RESPONSE-BODY: ")
        self.print_val(response.json())
        if response.status_code == 404:
            return response.json()

        if response.status_code in [200, 201]:
            return response.json()
            # return self._parse_json(response)
        else:
            body = response.json()
            return body 

    def print_val(self, param):
        # print(param)
        pass
