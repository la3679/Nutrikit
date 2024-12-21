import unittest
from tests.utilities.requests_utils import post_rest_call,get_rest_call,delete_rest_call

class Test2(unittest.TestCase):
    def test_0_get_item(self):
        results, status = get_rest_call(self, f'http://localhost:5000/items/2')
        print(results)

    def test_1_add_items(self):
        request_body = {
            "item_name": "Egg",
            "item_type": "FOOD",
            "item_category": "PROTEINS",
            "unit": "1",
            "protein": 6,
            "carbohydrates": 0.6,
            "fats": 5
        }
        results, status = post_rest_call(self, f'http://localhost:5000/items', json=request_body)
        print(results)
        post_body = {
            "item_name": "Apple",
            "item_type": "FOOD",
            "item_category": "FRUITS",
            "unit": "1",
            "protein": 1,
            "carbohydrates": 25,
            "fats": 0
        }
        results, status = post_rest_call(self, f'http://localhost:5000/items', json=post_body)
        # post_body2 = {
        #     "item_id": 1,
        #     "tag": "This a a fruit",
        # }
        # results= post_rest_call(self, f'http://localhost:5000/foodcategory', json=post_body2)
        print(results)
        post_body = {
            "item_name": "Chicken",
            "item_type": "FOOD",
            "item_category": "PROTEINS",
            "unit": "100g",
            "protein": 31.02,
            "carbohydrates": 0,
            "fats": 3.57
        }
        results, status = post_rest_call(self, f'http://localhost:5000/items', json=post_body)
        print(results)
        post_body = {
            "item_name": "Grapes",
            "item_type": "FOOD",
            "item_category": "FRUITS",
            "unit": "100g",
            "protein": 0.6,
            "carbohydrates": 17,
            "fats": 0.2
        }
        results, status = post_rest_call(self, f'http://localhost:5000/items', json=post_body)
        print(results)

    def test_2_list_items(self):
        results, status = get_rest_call(self, f'http://localhost:5000/items')
        print(results)

    def test_2_delete_item(self):
        results, status = delete_rest_call(self,f"http://localhost:5000/items/2")
        print(results)