import pandas as pd
import pulp
try:
    from db.ItemRepository import *
    from utilities.requests import post_rest_call_with_auth, post_rest_call
    from model.DietPlan import DietPlan
    from utilities.swen610_db_utils import * 
except ImportError:
    from src.db.ItemRepository  import *
    from src.model.DietPlan import DietPlan
    from src.utilities.swen610_db_utils import *
    from src.model.DietPlan import DietPlan

class DietPlanRepository:
    table = "diet_plans"

    def create(diet_plan: DietPlan):
        json_data = {}
        for key, value in diet_plan.__dict__.items():
            if value is None:
                continue
            json_data[key.replace("_DietPlan__", "")] = value
        df = pd.DataFrame.from_dict([json_data])
        id = commit_dataframe(df, DietPlanRepository.table)
        return id

    def get_by_id(id) :
        query = """
        SELECT id, diet_goal_id, item_id, time_to_consume, amount
        FROM diet_plans 
        WHERE id=%s;
        """
        values = (id,)
        result = exec_get_one(query, values)
        if result is not None:
            diet_plan = DietPlan(
                id=result[0],
                diet_goal_id= result[1],
                item_id= result[2],
                time_to_consume= result[3],
                amount=result[4]
            )
            return diet_plan
        return None

    def get_by_diet_goal_id(id):
        query = """
        SELECT id, diet_goal_id, item_id, time_to_consume, amount
        FROM diet_plans 
        WHERE diet_goal_id=%s;
        """
        values = (id,)
        results = exec_get_all(query, values)
        if results is not None:
            return [DietPlan(
                id=result[0],
                diet_goal_id= result[1],
                item_id= result[2],
                time_to_consume= result[3],
                amount=result[4]
            ) for result in results]
        return None

    def delete(diet_plan: DietPlan):
        query = """
        DELETE 
        FROM diet_plans 
        WHERE id=%s;
        """
        values = (diet_plan.id,)
        result = exec_commit(query, values)
        return result
    
    def auto_generate_plan(self,calories,protein,carbs,fats):
        itemrepo= ItemRepository()
        meals, food_items = itemrepo.get_optimization_food_items()
        goals = {
            'protein': protein,  # in grams
            'carbs': carbs,   # in grams
            'fats': fats,     # in grams
            'calories': calories # in kcal
        }
        problem = pulp.LpProblem("Diet Optimization", pulp.LpMinimize)
        meal_vars = pulp.LpVariable.dicts("Meal", meals.keys(), 0, 1, pulp.LpInteger)
        # Decision variables for food items
        food_vars = {}
        for food, properties in food_items.items():
            if properties['type'] == 'Continuous':
                food_vars[food] = pulp.LpVariable(f"Food_{food}", lowBound=properties['serving_size']/properties['per']/4)
                problem += food_vars[food] <= properties['MaxAverage'], f"MaxAvg_{food}"
            elif properties['type'] == 'Discrete':
                food_vars[food] = pulp.LpVariable(f"Food_{food}", lowBound=0, cat=pulp.LpInteger)
        # Constraints for meal types
        problem += pulp.lpSum([meal_vars[meal] for meal in meals if meals[meal]['type'] == 'Breakfast']) == 1
        problem += pulp.lpSum([meal_vars[meal] for meal in meals if meals[meal]['type'] == 'Lunch']) == 1
        problem += pulp.lpSum([meal_vars[meal] for meal in meals if meals[meal]['type'] == 'Dinner']) == 1
        problem += pulp.lpSum([meal_vars[meal] for meal in meals if meals[meal]['type'] == 'Snack']) <= 2
        deviation_vars = pulp.LpVariable.dicts("Deviation", goals.keys(), lowBound=0)
        # Calorie constraint within 100 kcal range
        problem += (pulp.lpSum([meal_vars[meal] * meals[meal]['calories'] for meal in meals]) +
                    pulp.lpSum([food_vars[food] * food_items[food]['calories'] for food in food_items])) >= goals['calories'] - 500, "MinCalories"
        problem += (pulp.lpSum([meal_vars[meal] * meals[meal]['calories'] for meal in meals]) +
                    pulp.lpSum([food_vars[food] * food_items[food]['calories'] for food in food_items])) <= goals['calories'] + 500, "MaxCalories"
        # Nutritional constraints (considering both meals and food items)
        for nutrient in ['protein', 'carbs', 'fats']:
            problem += (pulp.lpSum([meal_vars[meal] * meals[meal][nutrient] for meal in meals]) +
                        pulp.lpSum([food_vars[food] * food_items[food][nutrient] for food in food_items])) >= goals[nutrient]
            problem += (pulp.lpSum([meal_vars[meal] * meals[meal][nutrient] for meal in meals]) +
                    pulp.lpSum([food_vars[food] * food_items[food][nutrient] for food in food_items])) <= goals[nutrient] + 40, f"Max_{nutrient}"
        for nutrient in ['protein', 'carbs', 'fats', 'calories']:
            nutrient_sum = pulp.lpSum([meal_vars[meal] * meals[meal][nutrient] for meal in meals]) + \
                        pulp.lpSum([food_vars[food] * food_items[food][nutrient] for food in food_items])
            problem += nutrient_sum >= goals[nutrient] - deviation_vars[nutrient]
            problem += nutrient_sum <= goals[nutrient] + deviation_vars[nutrient]     
        problem += pulp.lpSum([deviation_vars[nutrient] for nutrient in goals])
        problem.solve()
        # Output the results
        if problem.status == pulp.LpStatusOptimal:
            solution={}
            solution['status']='OK'
            solution['type']= 'DB'
            solution['Main dishes']={'instructions':'These to be eaten as your main breakfast,lunch,dinner and snacks','list':[]}
            solution['Additions']={'instructions':'These to be fitted to your schedule as you enjoy','list':[]}
            total_cal=0
            total_carb=0
            total_fat=0
            total_pro=0
            print("Optimal diet plan:")
            for meal in meal_vars:
                if meal_vars[meal].value() > 0:
                    solution['Main dishes']['list'].append({'type':meals[meal]['type'],
                                    'name':meal,
                                    'calories':meals[meal]['calories'],
                                    'carbs':meals[meal]['carbs'],
                                    'protein':meals[meal]['protein'],
                                    'fats':meals[meal]['fats'],
                                    'quantity': meal_vars[meal].value()
                                    })
                    total_cal+=meals[meal]['calories']*meal_vars[meal].value()
                    total_carb+=meals[meal]['carbs']*meal_vars[meal].value()
                    total_fat+=meals[meal]['fats']*meal_vars[meal].value()
                    total_pro+=meals[meal]['protein']*meal_vars[meal].value()
            for food in food_vars:
                if food_vars[food].value() > 0:
                    solution['Additions']['list'].append({
                                    'name':food,
                                    'calories':food_items[food]['calories'],
                                    'carbs':food_items[food]['carbs'],
                                    'protein':food_items[food]['protein'],
                                    'fats':food_items[food]['fats'],
                                    'quantity':round(food_vars[food].value()*food_items[food]['serving_size']) if food_items[food]['type'] =='Continuous' else food_vars[food].value(),
                                    'unit':'grams'
                                    })
                    total_cal+=food_items[food]['calories']*food_vars[food].value()
                    total_carb+=food_items[food]['carbs']*food_vars[food].value()
                    total_fat+=food_items[food]['fats']*food_vars[food].value()
                    total_pro+=food_items[food]['protein']*food_vars[food].value()
            solution['Nutrition info']={'Total calories':round(total_cal),'Total carbs':round(total_carb),'Total fats':round(total_fat),'Total protein':round(total_pro)}
            return solution
        else:
            return None
    
    def third_party_plans(self,calories,protein,carbs,fats,tolerance=0.2):
        app_id= '84e5ab0c'
        app_key= '36dc033475ea4ebceeba3b4a24078fdb'
        field= ['label','totalNutrients']
        plan_url = f'https://api.edamam.com/api/meal-planner/v1/{app_id}/select'
        recipe_url= 'https://api.edamam.com/api/recipes/v2/by-uri'
        userid='tahh1'
        type='public'
        request = {    "size": 1,    
        "plan": {   
            "accept": {   "all": [                           ]        },
                            "fit": {            
                                "ENERC_KCAL": {"min": calories-calories*tolerance, "max": calories+calories*tolerance},
                                "PROCNT": {"min": protein-protein*tolerance, "max": protein+protein*tolerance},
                                "FAT": {"min": fats-fats*tolerance, "max":  fats+fats*tolerance},
                                "CHOCDF": {"min": carbs-carbs*tolerance, "max": carbs+carbs*tolerance}        },        
                                "sections": {            
                                    "Breakfast": {   "accept": {       "all": [           {"meal": [ "breakfast" ]}       ]   }, 
                                                    "fit": {   }},
                                        "Lunch": {   
                                            "accept": {       
                                                "all": [           {"meal": [ "lunch/dinner" ]}       ]   },   
                                                "fit": {     }},
                                        "Dinner": {   "accept": {
                                                   "all": [          {"meal": [ "lunch/dinner" ]}       ]   },   
                                                        "fit": {   }}        }    }}
        headers = {'Edamam-Account-User':userid}
        response, status= post_rest_call_with_auth(plan_url,app_id,app_key,post_header=headers,json=request)
        if(status==200 and response['status']=='OK'):
            dishes= {key:val['assigned'] for key,val in response['selection'][0]['sections'].items()}
            dishes['Status']= 'OK'
            dishes['type']= 'API'
            for key,value in dishes.items():
                params={"field":field,"uri":value,"app_key":app_key,"app_id":app_id, "type":type, "uri":value}
                headers = {'Edamam-Account-User':userid,"Accept-Language":"eng"}
                response, status= post_rest_call(recipe_url,params=params,post_header=headers)
                print(response)
                print(status)
                if(status==200):
                    print(response)
                    dishes[key] = response['hits'][0]['recipe']
                else:
                    dishes[key]+=":\t could not be fetched"
                    continue
            return dishes
        return None
