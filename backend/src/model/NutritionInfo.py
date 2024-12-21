class NutritionInfo:
    def __init__(self, unit, protein, carbs, fats, id=None, item_id=None):
        """

        @param item_id:
        @param unit:
        @param protein:
        @param carbs:
        @param fats:
        @param id:
        """
        self.id = id
        self.item_id = item_id
        self.unit = unit
        self.protein = protein
        self.carbs = carbs
        self.fats = fats