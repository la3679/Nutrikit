import datetime
try:
    from utilities.parsers import tracked_item_parser
    from utilities.swen610_db_utils import exec_get_one, exec_commit, exec_get_all, exec_fetch
except ImportError:
    from src.utilities.parsers import tracked_item_parser
    from src.utilities.swen610_db_utils import exec_get_one, exec_commit, exec_get_all, exec_fetch

class DietTracker:
    def __init__(self,user_id):
        self.user_id= user_id

    def add_consumed_item(self,item_id,amount,consumed_time=datetime.datetime.now()):
        sql="INSERT INTO diet_trackers(user_id,item_id,consumed_time,amount) \
        VALUES (%s,%s,TO_TIMESTAMP(%s,'MM/DD/YYYY HH:MI'),%s) RETURNING id;"
        print(type(consumed_time))
        entry_id = exec_fetch(sql,(self.user_id,item_id,datetime.datetime.strftime(consumed_time,"%m/%d/%Y %I:%M"),amount,))[0]
        return   {
        "entry_id":entry_id, 
        "item_id":item_id,
        "consumed_time": datetime.datetime.strftime(consumed_time,'%m/%d/%Y %H:%M'),
        "amount": amount
    }
        
    def get_comsumption(self):
        sql="""SELECT d.id, d.item_id, i.item_name, i.item_type, d.consumed_time, d.amount,
            i.item_category, j.protein, j.carbs, j.fats
            FROM diet_trackers d
            JOIN items i ON d.item_id = i.id
            JOIN nutrition_info j ON d.item_id = j.item_id
            WHERE user_id=%s and DATE(consumed_time) = CURRENT_DATE """
        items=exec_get_all(sql,(self.user_id,))
        if(len(items)>0):
            tracked_items= [tracked_item_parser(item) for item in items]
            return tracked_items
        return []
    
    def delete_item(self,entry_id):
        sql="DELETE FROM diet_trackers WHERE id=%s and user_id=%s;"
        exec_commit(sql,(entry_id,self.user_id,))

    def modify_amount(self,entry_id,new_amount):
        sql = "UPDATE diet_trackers SET amount = %s WHERE id=%s and user_id = %s;"
        exec_commit(sql,(new_amount,entry_id,self.user_id,))

        

