try:
    from model.Item import Item
    from model.NutritionInfo import NutritionInfo
    from utilities.swen610_db_utils import *
except ImportError:
    from src.model.Item import Item
    from src.model.NutritionInfo import NutritionInfo
    from src.utilities.swen610_db_utils import *


class NutritionInfoRepository:
    table = "nutrition_info"

    def get_by_id(id):
        query = """
        SELECT id, item_id, unit, protein, carbs, fats
        FROM nutrition_info 
        WHERE id=%s;
        """
        values = (id,)
        result = exec_get_one(query, values)
        if result is not None:
            nutri_info = NutritionInfo(
                id=result[0],
                item_id=result[1],
                unit=result[2],
                protein=result[3],
                carbs=result[4],
                fats=result[5]
            )
            return nutri_info
        return None

    def get_by_item_id(item_id):
        query = """
        SELECT id, item_id, unit, protein, carbs, fats
        FROM nutrition_info 
        WHERE item_id=%s;
        """
        values = (item_id,)
        result = exec_get_one(query, values)
        if result is not None:
            nutri_info = NutritionInfo(
                id=result[0],
                item_id=result[1],
                unit=result[2],
                protein=result[3],
                carbs=result[4],
                fats=result[5]
            )
            return nutri_info
        return None

    def get_all():
        query = """
        SELECT id, item_id, unit, protein, carbs, fats
        FROM nutrition_info 
        """
        values = (id,)
        results = exec_get_all(query, values)
        if results is not None:
            return [NutritionInfo(
                id=result[0],
                item_id=result[1],
                unit=result[2],
                protein=result[3],
                carbs=result[4],
                fats=result[5]
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