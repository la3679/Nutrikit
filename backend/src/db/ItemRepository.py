import pandas as pd
try:
    from model.Item import Item, ITEM_TYPE, ITEM_CATEGORY
    from model.NutritionInfo import NutritionInfo
    from db.NutritionInfoRepository import NutritionInfoRepository
    from utilities.swen610_db_utils import *
except ImportError:
    from src.model.Item import Item, ITEM_TYPE, ITEM_CATEGORY
    from src.model.NutritionInfo import NutritionInfo
    from src.db.NutritionInfoRepository import NutritionInfoRepository
    from src.utilities.swen610_db_utils import *

class ItemRepository:
    table = "items"
    nutri_table = "nutrition_info"

    def create(item: Item, nutrition_info: NutritionInfo):
        json_data = {}
        for key, value in item.__dict__.items():
            if value is None:
                continue
            json_data[key.replace("_Item__", "")] = value
        df = pd.DataFrame.from_dict([json_data])
        id = commit_dataframe(df, ItemRepository.table)
        nutrition_info.item_id = id
        json_data = {}
        for key, value in nutrition_info.__dict__.items():
            if value is None:
                continue
            json_data[key.replace("_NutritionInfo__", "")] = value
        df = pd.DataFrame.from_dict([json_data])
        nutri_id = commit_dataframe(df, ItemRepository.nutri_table)
        return id, nutri_id

    def get_by_id(id) :
        query = """
        SELECT id, item_name, item_type, item_category
        FROM items 
        WHERE id=%s;
        """
        values = (id,)
        result = exec_get_one(query, values)
        if result is not None:
            item = Item(
                id=result[0],
                item_name= result[1],
                item_type= ITEM_TYPE[result[2]],
                item_category= ITEM_CATEGORY[result[3]],
            )
            return item
        return None

    def get_all():
        query = """
        SELECT id, item_name, item_type, item_category
        FROM items 
        """
        values = (id,)
        results = exec_get_all(query, values)
        if results is not None:
            return [Item(
                id=result[0],
                item_name=result[1],
                item_type= ITEM_TYPE[result[2]],
                item_category= ITEM_CATEGORY[result[3]],
            ) for result in results]
        return None

    def delete(item: Item):
        query = """
        DELETE 
        FROM items 
        WHERE id=%s;
        """
        values = (item.id,)
        result = exec_commit(query, values)
        return result
    
    def get_optimization_food_items(self):
        meals = {
        'Oatmeal Breakfast': {'type': 'Breakfast', 'protein': 6, 'carbs': 25, 'fats': 3, 'calories': 150},
        'Chicken Salad Lunch': {'type': 'Lunch', 'protein': 30, 'carbs': 10, 'fats': 15, 'calories': 350},
        'Steak Dinner': {'type': 'Dinner', 'protein': 45, 'carbs': 5, 'fats': 20, 'calories': 400},
        'Yogurt Snack': {'type': 'Snack', 'protein': 10, 'carbs': 15, 'fats': 5, 'calories': 100},
        'Vegan Wrap': {'type': 'Lunch', 'protein': 12, 'carbs': 35, 'fats': 9, 'calories': 290},
        'Granola Bar': {'type': 'Snack', 'protein': 3, 'carbs': 20, 'fats': 6, 'calories': 150},
        'Pasta Carbonara': {'type': 'Dinner', 'protein': 20, 'carbs': 45, 'fats': 18, 'calories': 410},
        'Fruit Salad Breakfast': {'type': 'Breakfast', 'protein': 2, 'carbs': 30, 'fats': 1, 'calories': 120},
        'Tofu Stir Fry': {'type': 'Dinner', 'protein': 18, 'carbs': 25, 'fats': 10, 'calories': 250},
        'Turkey Sandwich': {'type': 'Lunch', 'protein': 25, 'carbs': 35, 'fats': 7, 'calories': 320},
        'Cheese Pizza': {'type': 'Dinner', 'protein': 16, 'carbs': 40, 'fats': 12, 'calories': 300},
        'Berry Smoothie': {'type': 'Snack', 'protein': 5, 'carbs': 18, 'fats': 2, 'calories': 100},
        'Egg and Avocado Toast': {'type': 'Breakfast', 'protein': 12, 'carbs': 30, 'fats': 15, 'calories': 300},
        'Quinoa Salad': {'type': 'Lunch', 'protein': 8, 'carbs': 40, 'fats': 6, 'calories': 230},
        'Fish Tacos': {'type': 'Dinner', 'protein': 22, 'carbs': 35, 'fats': 9, 'calories': 350},
        'Trail Mix Snack': {'type': 'Snack', 'protein': 7, 'carbs': 20, 'fats': 15, 'calories': 200},
        'Greek Salad': {'type': 'Lunch', 'protein': 6, 'carbs': 20, 'fats': 10, 'calories': 180},
        'Pancakes with Syrup': {'type': 'Breakfast', 'protein': 6, 'carbs': 50, 'fats': 8, 'calories': 300},
        'Vegetable Curry': {'type': 'Dinner', 'protein': 10, 'carbs': 45, 'fats': 15, 'calories': 360},
        'Protein Shake': {'type': 'Snack', 'protein': 20, 'carbs': 5, 'fats': 2, 'calories': 120}
        }


        food_items = {
        'Apple': {'type': 'Discrete', 'protein': 0.3, 'carbs': 14, 'fats': 0.2, 'calories': 52, 'MaxAverage': 4, 'per': 1 },
        'Chicken Breast': {'type': 'Continuous', 'protein': 31, 'carbs': 0, 'fats': 3.6, 'calories': 165, 'MaxAverage': 500, 'serving_size': 150, 'per': 150},
        'Brown Rice': {'type': 'Continuous', 'protein': 2.6, 'carbs': 23, 'fats': 0.9, 'calories': 110, 'MaxAverage': 300, 'serving_size': 100, 'per': 100},
        'Boiled Egg': {'type': 'Discrete', 'protein': 6.3, 'carbs': 0.6, 'fats': 5.3, 'calories': 77, 'MaxAverage': 6, 'per': 1 },
        'Almonds': {'type': 'Continuous', 'protein': 21, 'carbs': 22, 'fats': 50, 'calories': 579, 'MaxAverage': 100, 'serving_size': 30, 'per': 30},
        'Greek Yogurt': {'type': 'Continuous', 'protein': 10, 'carbs': 4, 'fats': 0.7, 'calories': 59, 'MaxAverage': 200, 'serving_size': 200, 'per': 200},
        'Spinach': {'type': 'Continuous', 'protein': 2.9, 'carbs': 3.6, 'fats': 0.4, 'calories': 23, 'MaxAverage': 200, 'serving_size': 30, 'per': 30},
        'Sweet Potato': {'type': 'Continuous', 'protein': 2, 'carbs': 20, 'fats': 0.1, 'calories': 86, 'MaxAverage': 300, 'serving_size': 200, 'per': 200},
        'Salmon': {'type': 'Continuous', 'protein': 20, 'carbs': 0, 'fats': 13, 'calories': 208, 'MaxAverage': 300, 'serving_size': 150, 'per': 150},
        'Quinoa': {'type': 'Continuous', 'protein': 4.4, 'carbs': 21, 'fats': 1.9, 'calories': 120, 'MaxAverage': 200, 'serving_size': 185, 'per': 185},
        'Banana': {'type': 'Discrete', 'protein': 1.3, 'carbs': 27, 'fats': 0.3, 'calories': 105, 'MaxAverage': 5, 'per': 1 },
        'Broccoli': {'type': 'Continuous', 'protein': 2.8, 'carbs': 6, 'fats': 0.4, 'calories': 31, 'MaxAverage': 250, 'serving_size': 90, 'per': 90},
        'Whole Wheat Bread': {'type': 'Continuous', 'protein': 13, 'carbs': 41, 'fats': 4.2, 'calories': 247, 'MaxAverage': 200, 'serving_size': 50, 'per': 50},
        'Avocado': {'type': 'Continuous', 'protein': 2, 'carbs': 9, 'fats': 15, 'calories': 160, 'MaxAverage': 3, 'serving_size': 150, 'per': 150},
        'Tofu': {'type': 'Continuous', 'protein': 8, 'carbs': 2, 'fats': 4, 'calories': 70, 'MaxAverage': 300, 'serving_size': 100, 'per': 100},
        'Cheddar Cheese': {'type': 'Continuous', 'protein': 25, 'carbs': 1.3, 'fats': 33, 'calories': 402, 'MaxAverage': 150, 'serving_size': 50, 'per': 50}
        }
        return meals, food_items
