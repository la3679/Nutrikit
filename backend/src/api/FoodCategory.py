from flask_restful import Resource,reqparse
from flask_restful import request
from db.FoodCategory import *

class FoodCategories(Resource):
    def get(self):
        result = FoodCategory.List_All_Food_Categories()
        return result


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_id', type=int)
        parser.add_argument('tag', type=str)
        args = parser.parse_args()
        item_id = args['item_id']
        tag = args['tag']
        return FoodCategory.Add_Food_Category(item_id,tag)


    def put(self, id):
        pass

    def delete(self):
        category_id = int(request.headers.get('category_id'))
        result = FoodCategory.Delete_Food_Category(category_id)
        return result

