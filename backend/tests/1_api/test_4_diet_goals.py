import unittest
import datetime
from tests.utilities.requests_utils import post_rest_call,get_rest_call,delete_rest_call,put_rest_call

class Test4(unittest.TestCase):
    def test_0_add_diet_goal(self):
        request_body = {
            "user_id": "ahad",
            "start_date": ((datetime.datetime.utcnow() - datetime.timedelta(days=30))).strftime('%m/%d/%Y'),
            "end_date": ((datetime.datetime.utcnow() + datetime.timedelta(days=60))).strftime('%m/%d/%Y'),
            "protein": 55,
            "fats": 60,
            "carbs": 300,
        }
        results, status = post_rest_call(self, f'http://localhost:5000/diet', json=request_body)
        print(results)
        request_body = {
            "user_id": "ahad",
            "start_date": (datetime.datetime.utcnow() + datetime.timedelta(days=30)).strftime('%m/%d/%Y'),
            "end_date": (datetime.datetime.utcnow() + datetime.timedelta(days=60)).strftime('%m/%d/%Y'),
            "protein": 55,
            "fats": 50,
            "carbs": 250,
        }
        results, status = post_rest_call(self, f'http://localhost:5000/diet', json=request_body)
        print(results)

    def test_1_get_diet_goals(self):
        headers = {
            "userid": "ahad"
        }
        results, status = get_rest_call(self, f'http://localhost:5000/diet/all', get_header=headers)
        print(results)

    def test_2_delete_diet_goal(self):
        params = {
            "id": 1,
        }
        results, status = delete_rest_call(self, f'http://localhost:5000/diet', params=params)
        print(results)

    def test_3_make_diet_goal_active(self):
        request_body = {
            "user_id": "ahad",
            "id": 2,
            "active": True
        }
        results, status = put_rest_call(self, f'http://localhost:5000/diet', json=request_body)
        print(results)

    def test_4_change_active_diet_goal(self):
        request_body = {
            "user_id": "ahad",
            "start_date": ((datetime.datetime.utcnow() - datetime.timedelta(days=60))).strftime('%m/%d/%Y'),
            "end_date": ((datetime.datetime.utcnow() + datetime.timedelta(days=90))).strftime('%m/%d/%Y'),
            "protein": 60,
            "fats": 60,
            "carbs": 350,
        }
        results, status = post_rest_call(self, f'http://localhost:5000/diet', json=request_body)
        print(results)
        request_body = {
            "user_id": "ahad",
            "id": 3,
            "active": True
        }
        results, status = put_rest_call(self, f'http://localhost:5000/diet', json=request_body)
        print(results)