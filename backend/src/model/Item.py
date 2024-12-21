from enum import Enum

class ITEM_TYPE(Enum):
    MEAL = "MEAL"
    FOOD = "FOOD"

class ITEM_CATEGORY(Enum):
    PROTEINS = "PROTEINS"
    FRUITS = "FRUITS"
    VEGETABLES = "VEGETABLES"
    DAIRY = "DAIRY"
    GRAINS = "GRAINS"

class Item:
    def __init__(self, item_name, item_type: ITEM_TYPE, item_category: ITEM_CATEGORY, id=None):
        """

        @param item_name:
        @param item_type:
        @param item_category:
        @param id:
        """
        self.id = id
        self.item_name = item_name
        self.item_type = item_type.value
        self.item_category = item_category.value