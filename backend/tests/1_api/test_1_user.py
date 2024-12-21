import unittest
from tests.utilities.requests_utils import post_rest_call, get_rest_call

class UserTest(unittest.TestCase):
    access_token = None
    # test login
    def test_0_get_user(self):
        results, status = get_rest_call(self, f'http://localhost:5000/users/ahad')
        print(results)

    def test_1_create_user(self):
        request_body = {
            "id": "jheel",
            "display_name": "Jheel Patel",
            "email": "jp9959@rit.edu",
            "password": "1234567"
        }
        results, status = post_rest_call(self, f'http://localhost:5000/users', json=request_body)
        print(results)

    def test_2_list_users(self):
        results, status = get_rest_call(self, f'http://localhost:5000/users')
        print(results)

    def test_3_login(self):
        request_body = {
            "id": "jheel",
            "password": "1234567"
        }
        results, status = post_rest_call(self, f'http://localhost:5000/auth/login', json=request_body)
        print(results)
        self.__class__.access_token = results["access_token"]
        request_body = {
            "id": "jheel",
            "access_token": self.__class__.access_token
        }
        results, status = post_rest_call(self, f'http://localhost:5000/auth/check_session', json=request_body)
        print(results)

    def test_3_login_incorrect_password(self):
        request_body = {
            "id": "ahad",
            "password": "1234567"
        }
        results, status = post_rest_call(self, f'http://localhost:5000/auth/login', json=request_body)
        print(results)

    def test_3_logout(self):
        request_body = {
            "id": "jheel",
        }
        results, status = post_rest_call(self, f'http://localhost:5000/auth/logout', json=request_body)
        print(results)
        request_body = {
            "id": "jheel",
            "access_token": self.__class__.access_token
        }
        results, status = post_rest_call(self, f'http://localhost:5000/auth/check_session', json=request_body)
        print(results)
        request_body = {
            "id": "jheel",
            "access_token": "NA"
        }
        results, status = post_rest_call(self, f'http://localhost:5000/auth/check_session', json=request_body)
        print(results)