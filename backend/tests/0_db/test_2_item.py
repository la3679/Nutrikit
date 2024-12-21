import unittest
from src.model.Item import Item, ITEM_TYPE, ITEM_CATEGORY
from src.model.NutritionInfo import NutritionInfo
from src.db.ItemRepository import ItemRepository
from src.db.NutritionInfoRepository import NutritionInfoRepository
from src.utilities.swen610_db_utils import exec_sql_file


class NutrikitSetupDB(unittest.TestCase):
    # setup test date from sql file and also sample rows
    def test_0_create_item(self):
        item = Item(
            item_name="Rice",
            item_category=ITEM_CATEGORY.GRAINS,
            item_type=ITEM_TYPE.FOOD
        )
        nutri_info = NutritionInfo(
            unit="100g", protein=3.5, carbs=35, fats=0.3
        )
        ItemRepository.create(item, nutri_info)

        item = Item(
            item_name="Milk",
            item_category=ITEM_CATEGORY.DAIRY,
            item_type=ITEM_TYPE.FOOD
        )
        nutri_info = NutritionInfo(
            unit="1cup", protein=8, carbs=12, fats=8
        )
        ItemRepository.create(item, nutri_info)

    def test_1_get_item_by_id(self):
        item = ItemRepository.get_by_id(2).__dict__
        nutri_info = NutritionInfoRepository.get_by_item_id(item["id"]).__dict__
        nutri_info.pop("id")
        item.update(nutri_info)
        print(item)

    def test_2_delete_item(self):
        item_id = 1
        item = ItemRepository.get_by_id(item_id)
        ItemRepository.delete(item)
