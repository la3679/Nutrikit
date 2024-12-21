import requests
# The client (unittest) can only contact the server using RESTful API calls


# For API calls using GET.  params and header are defaulted to 'empty'

def get_rest_call(test, url, params = {}, get_header = {}):
    response = requests.get(url, params, headers = get_header)
    # test.assertEqual(expected_code, response.status_code,
    #                  f'Response code to {url} not {expected_code}')
    return response.json(), response.status_code

# For API calls using POST.  params and header are defaulted to 'empty'

def post_rest_call(test, url, params = {}, post_header = {}, json={}):
    '''Implements a REST api using the POST verb'''
    response = requests.post(url, json=json, headers = post_header)
    # test.assertEqual(expected_code, response.status_code,
    #                  f'Response code to {url} not {expected_code}')
    return response.json(), response.status_code

# For API calls using PUT.  params and header are defaulted to 'empty'

def put_rest_call(test, url, params = {}, put_header = {}, json={}):
    '''Implements a REST api using the PUT verb'''
    response = requests.put(url, json=json, headers = put_header)
    # test.assertEqual(expected_code, response.status_code,
    #                  f'Response code to {url} not {expected_code}')
    return response.json(), response.status_code

# For API calls using DELETE.  header is defaulted to 'empty'

def delete_rest_call(test, url, delete_header={}, json={}, params={}):
    '''Implements a REST api using the DELETE verb'''
    response = requests.delete(url, headers = delete_header, json=json, params=params)
    # test.assertEqual(expected_code, response.status_code,
    #                  f'Response code to {url} not {expected_code}')
    return response.json(), response.status_code
