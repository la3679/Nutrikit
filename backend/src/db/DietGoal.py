import datetime
try:
    from utilities.parsers import diet_goal_parser
    from utilities.swen610_db_utils import exec_get_one, exec_commit, exec_get_all, exec_fetch
except ImportError:
    from src.utilities.parsers import diet_goal_parser
    from src.utilities.swen610_db_utils import exec_get_one, exec_commit, exec_get_all, exec_fetch


class DietGoal:
    def __init__(self,id=None,user_id=None,start_date=None,end_date=None,active=None,protein=None,fats=None,carbs=None):
        self.id=id
        self.user_id=user_id
        self.start_date=start_date
        self.end_date=end_date
        self.active=active
        self.protein=protein
        self.fats=fats
        self.carbs=carbs

    def add_diet_goal(self):
        query="""INSERT INTO diet_goals(user_id,start_date,end_date,active,protein,fats,carbs) 
        values(%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
        values=(self.user_id,self.start_date,self.end_date,self.active,self.protein,self.fats,self.carbs,)
        self.id = exec_fetch(query, values)[0]
        return self.to_dict()
    
    def get_diet_goal(self):
        query ="SELECT * FROM diet_goals WHERE id=%s ORDER BY active DESC"
        values=(self.id,)
        diet=exec_get_one(query,values)
        if(diet!=None):
            self.user_id=diet[1]
            self.start_date=diet[2]
            self.end_date=diet[3]
            self.active=diet[4]
            self.protein=diet[5]
            self.fats=diet[6]
            self.carbs=diet[7]
            diet_goal_obj= self.to_dict()
            return diet_goal_obj
        return None 
    
    def get_user_goals_list(self):
        query="SELECT * FROM diet_goals WHERE user_id=%s ORDER BY active DESC"
        values=(self.user_id,)
        diets=exec_get_all(query,values)
        if(len(diets)>0):
            diet_goals= [ diet_goal_parser(diet) for diet in diets]
            return diet_goals
        return []
    
    def delete_user_diet_goal(self):
        query="DELETE FROM diet_goals WHERE id=%s"
        values=(self.id,)
        exec_commit(query,values)
        return []

    def modify_diet_goals(self,kwargs):
        if(len(kwargs)>0):
            query="UPDATE diet_goals SET "
            values=()
            for key,value in kwargs.items():
                query+=f"{key}=COALESCE(%s, {key}),"
                values += (value,)
            query= query[:-1]+ " WHERE id=%s;"
            print(query)
            values+=(self.id,)
            exec_commit(query,values)
    @staticmethod
    def get_active_diet_goal(user_id):
        query ="SELECT * FROM diet_goals WHERE user_id=%s and active=True"
        values=(user_id,)
        diet=exec_get_one(query,values)
        diet_goal = DietGoal()
        if(diet!=None):
            diet_goal.id=diet[0]
            diet_goal.user_id=diet[1]
            diet_goal.start_date=diet[2]
            diet_goal.end_date=diet[3]
            diet_goal.active=diet[4]
            diet_goal.protein=diet[5]
            diet_goal.fats=diet[6]
            diet_goal.carbs=diet[7]
            return diet_goal
        return None 


    def to_dict(self):
        return {
        "id": self.id,
        "start_date": datetime.datetime.strftime(self.start_date,'%m/%d/%Y') if self.start_date!= None else None,
        "end_date": datetime.datetime.strftime(self.end_date,'%m/%d/%Y') if self.start_date!= None else None,
        "active": self.active,
        "protein": self.protein,
        "fats": self.fats,
        "carbs": self.carbs,
        }
    

        

