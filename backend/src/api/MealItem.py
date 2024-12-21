from flask_restful import Resource,reqparse
from flask_restful import request
from db.MealItem import *

class MealItem(Resource):
    def get(self):
        result = MealItems.List_All_Meal_Item()
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int)
        parser.add_argument('meal_name', type=str)
        parser.add_argument('quantity', type=int)
        args = parser.parse_args()
        item_id = args['item_id']
        meal_name = args['meal_name']
        quantity = args['quantity']
        return MealItems.Add_Meal_Item(item_id,meal_name,quantity)

    def put(self):
        pass

    def delete(self):
        meal_id = int(request.headers.get('meal_id'))
        result = MealItems.Delete_Meal_Item(meal_id)
        return result