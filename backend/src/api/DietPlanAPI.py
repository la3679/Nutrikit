import json
from flask import Response
from flask_restful import Resource, reqparse
try:
    from db.DietPlanRepository import *
except ImportError:
    from src.db.DietPlanRepository import *

class DietPlan(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(DietPlan).__init__()
    def get(self):
        self.reqparse.add_argument('calories', type = float, required = True,
            location = 'json')
        self.reqparse.add_argument('carbs', type = float, required = True,
            location = 'json')
        self.reqparse.add_argument('fats', type = float, required = True,
            location = 'json')
        self.reqparse.add_argument('protein', type = float, required = True,
            location = 'json')
        self.reqparse.add_argument('source', type = str, required = True,
            location = 'json')
        args= self.reqparse.parse_args()
        dietplanrepo= DietPlanRepository()
        source = args['source']
        if(source=='db'):
            plan = dietplanrepo.auto_generate_plan(args['calories'],args['protein'],args['carbs'],args['fats'])
            if (plan!=None):
                return plan
            else:
                return {"message: We couldn't generate an appropriate diet from DB for you, try the api"}
        elif(source=='api'):
            plan =  dietplanrepo.third_party_plans(args['calories'],args['protein'],args['carbs'],args['fats'])
            if (plan!=None):
                return plan
            else:
                return {"message: We couldn't generate an appropriate diet from api for you, try the db"}
            
        elif(source=='any'):
            plan = dietplanrepo.auto_generate_plan(args['calories'],args['protein'],args['carbs'],args['fats'])
            if (plan!=None):
                return plan
            else:
                plan = dietplanrepo.third_party_plans(args['calories'],args['protein'],args['carbs'],args['fats'])
                if (plan!=None):           
                    return plan
                else:
                    return {"message: We couldn't generate an appropriate diet for you"}
