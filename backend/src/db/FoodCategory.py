from utilities.swen610_db_utils import *

class FoodCategory:
    def List_All_Food_Categories():
        return exec_get_all('SELECT * FROM item_tags;')
    
    def Add_Food_Category(item_id,tag):
        tuple_1= (item_id,tag)
        query_1= 'INSERT INTO item_tags (item_id,tag) VALUES (%s,%s);'
        exec_commit(query_1,tuple_1)
        return "Food Category Added"
    
    def Delete_Food_Category(id):
        exec_commit('DELETE FROM item_tags WHERE id = {}'.format(id))
        return True
