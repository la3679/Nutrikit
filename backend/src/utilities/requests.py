import requests
from requests.auth import HTTPBasicAuth
def post_rest_call_with_auth(url, username,password,params = {}, post_header = {}, json={}):
    '''Implements a REST api using the POST verb'''
    response = requests.post(url, json=json, headers = post_header,params=params,auth=HTTPBasicAuth(username, password))
    # test.assertEqual(expected_code, response.status_code,
    #                  f'Response code to {url} not {expected_code}')
    return response.json(), response.status_code



def post_rest_call(url, params = {}, post_header = {}, json={}):
    '''Implements a REST api using the POST verb'''
    response = requests.get(url, json=json, headers = post_header, params=params)
    # test.assertEqual(expected_code, response.status_code,
    #                  f'Response code to {url} not {expected_code}')
    return response.json(), response.status_code