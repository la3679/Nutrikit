import json
from flask import Response, request
from flask_restful import Resource
try:
    from db.ItemRepository import ItemRepository
    from db.NutritionInfoRepository import NutritionInfoRepository
    from model.Item import Item, ITEM_TYPE, ITEM_CATEGORY
    from model.NutritionInfo import NutritionInfo
except ImportError:
    from src.db.ItemRepository import ItemRepository
    from src.db.NutritionInfoRepository import NutritionInfoRepository
    from src.model.Item import Item, ITEM_TYPE, ITEM_CATEGORY
    from src.model.NutritionInfo import NutritionInfo

class ItemAPI(Resource):
    def get(self, id: str):
        item = ItemRepository.get_by_id(id)
        print(item)
        nutri_info = NutritionInfoRepository.get_by_item_id(item_id=item.id).__dict__
        nutri_info.pop("id")
        json_data = {}
        for key, value in item.__dict__.items():
            if key.find("_Item__") != -1:
                continue
            json_data[key] = value
        for key, value in nutri_info.items():
            if key.find("_NutritionInfo__") != -1:
                continue
            json_data[key] = value
        return Response(json.dumps(json_data), status=200, mimetype="application/json")

    def delete(self, id):
        item = ItemRepository.get_by_id(id)
        return ItemRepository.delete(item)

class ItemsAPI(Resource):
    def get(self):
        items = ItemRepository.get_all()
        json_data = []
        for item in items:
            temp = {}
            for key, value in item.__dict__.items():
                if key.find("_Item__") != -1:
                    continue
                temp[key] = value
            nutri_info = NutritionInfoRepository.get_by_item_id(item_id=item.id).__dict__
            nutri_info.pop("id")
            temp.update(nutri_info)
            json_data.append(temp)
        return Response(json.dumps(json_data), status=200, mimetype="application/json")

    def post(self):
        request_body = request.get_json()
        print(request_body)
        item = Item(
            item_name=request_body["item_name"],
            item_type=ITEM_TYPE[request_body["item_type"]],
            item_category=ITEM_CATEGORY[request_body["item_category"]]
        )
        nutri_info = NutritionInfo(
            unit=request_body["unit"],
            protein=request_body.get("protein"),
            carbs=request_body.get("carbohydrates"),
            fats=request_body.get("fats")
        )
        item_id, nutri_id = ItemRepository.create(item, nutri_info)
        item = ItemRepository.get_by_id(item_id)
        nutri_info = NutritionInfoRepository.get_by_item_id(item_id=item.id).__dict__
        nutri_info.pop("id")
        json_data = {}
        for key, value in item.__dict__.items():
            if key.find("_Item__") != -1:
                continue
            json_data[key] = value
        for key, value in nutri_info.items():
            if key.find("_NutritionInfo__") != -1:
                continue
            json_data[key] = value
        return Response(json.dumps(json_data), status=200, mimetype="application/json")