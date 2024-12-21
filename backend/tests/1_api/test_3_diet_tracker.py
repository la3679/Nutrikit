import unittest
from tests.utilities.requests_utils import post_rest_call,get_rest_call,delete_rest_call

class Test3(unittest.TestCase):
    def test_0_track_item(self):
        request_body = {
            "user_id": "ahad",
            "item_id": 3,
            "amount": 2,
        }
        results, status = post_rest_call(self, f'http://localhost:5000/tracker', json=request_body)
        print(results)

    def test_1_get_tracker(self):
        headers = {
            "userid": "ahad"
        }
        results, status = get_rest_call(self, f'http://localhost:5000/tracker', get_header=headers)
        print(results)

    def test_2_delete_tracked_item(self):
        request_body = {
            "user_id": "ahad",
            "entry_id": 3,
        }
        results, status = delete_rest_call(self, f'http://localhost:5000/tracker', json=request_body)
        print(results)