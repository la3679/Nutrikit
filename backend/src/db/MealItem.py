from utilities.swen610_db_utils import *

class MealItems:
    def List_All_Meal_Item():
        return exec_get_all('SELECT * FROM meal_components;')
    
    def Add_Meal_Item(item_id,meal_name,quantity):
        tuple_1= (item_id,meal_name,quantity)
        query_1= 'INSERT INTO meal_components (item_id,meal_name,quantity) VALUES (%s,%s,%s);'
        exec_commit(query_1,tuple_1)
        return "Meal Item Added"
    
    def Delete_Meal_Item(id):
        exec_commit('DELETE FROM meal_components WHERE id = {}'.format(id))
        return True
