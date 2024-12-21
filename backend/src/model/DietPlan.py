from datetime import datetime

class DietPlan:
    def __init__(self, time_to_consume: datetime, amount: float, diet_goal_id, item_id, id=None):
        """

        @param time_to_consume:
        @param amount:
        @param diet_goal_id:
        @param item_id:
        @param id:
        """
        self.id = id
        self.diet_goal_id = diet_goal_id
        self.item_id = item_id
        self.time_to_consume = time_to_consume
        self.amount = amount
