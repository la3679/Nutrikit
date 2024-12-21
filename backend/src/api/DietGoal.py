import json
from flask import Response
from flask_restful import Resource, reqparse
try:
    from db.DietGoal import *
except ImportError:
    from src.db.DietGoal import *

class DietGoalManagement(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(DietGoalManagement, self).__init__()
    def get(self):
        self.reqparse.add_argument('id', type = int, required = True,
            location = 'headers', help='diet goal id is required')
        args = self.reqparse.parse_args()
        id = args['id']
        dietgoal = DietGoal(id)
        goal = dietgoal.get_diet_goal()
        if(goal==None):
            return {'message':'Diet goal not found'}, 404
        return goal, 200

    def post(self):
        self.reqparse.add_argument('user_id', type = str, required = True,
            location = 'json')
        self.reqparse.add_argument('start_date', type = lambda x: datetime.datetime.strptime(x,'%m/%d/%Y'), required = True,
            location = 'json')
        self.reqparse.add_argument('end_date', type = lambda x: datetime.datetime.strptime(x,'%m/%d/%Y'), required = True,
            location = 'json')
        self.reqparse.add_argument('protein', type = float, required = True,
            location = 'json')
        self.reqparse.add_argument('fats', type = float, required = True,
            location = 'json')
        self.reqparse.add_argument('carbs', type = float, required = True,
            location = 'json')
        args = self.reqparse.parse_args()
        diet_goal = DietGoal(
            user_id=args['user_id'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            protein=args['protein'],
            fats=args['fats'],
            carbs=args['carbs'],
        )
        diet_goal.active = True if DietGoal.get_active_diet_goal(diet_goal.user_id) == None else False
        diet_goal_VM= diet_goal.add_diet_goal()
        return diet_goal_VM, 201

    def put(self):
        self.reqparse.add_argument('user_id', type = str, required = True,
            location = 'json')
        self.reqparse.add_argument('id', type = int, required = True,
            location = 'json')
        self.reqparse.add_argument('start_date', type = lambda x: datetime.datetime.strptime(x,'%m/%d/%Y'), required = False,
            location = 'json')
        self.reqparse.add_argument('end_date', type = lambda x: datetime.datetime.strptime(x,'%m/%d/%Y'), required = False,
            location = 'json')
        self.reqparse.add_argument('protein', type = float, required = False,
            location = 'json')
        self.reqparse.add_argument('fats', type = float, required = False,
            location = 'json')
        self.reqparse.add_argument('carbs', type = float, required = False,
            location = 'json')
        self.reqparse.add_argument('active', type = bool, required = False,
            location = 'json')
        args= self.reqparse.parse_args()
        diet_goal = DietGoal(args['id'])
        if(args['active']!=None and DietGoal.get_active_diet_goal(args['user_id'])!=None):
            active_diet_goal = DietGoal.get_active_diet_goal(args['user_id'])
            active_diet_goal.modify_diet_goals({'active': False})
        kwargs={}
        for key,val in args.items():
            if(val!=None):
                kwargs[key]=val
        diet_goal.modify_diet_goals(kwargs=kwargs)
        goal = diet_goal.get_diet_goal()
        # return goal_dict, 204
        return Response(json.dumps(goal), status=200, mimetype="application/json")
    
    def delete(self):
        self.reqparse.add_argument('id', type = int, required = True,
            location = 'args')
        args= self.reqparse.parse_args()
        diet_goal = DietGoal(args['id'])
        diet_goal.delete_user_diet_goal()
        return Response(json.dumps({
            "message": "SUCCESS"
        }), status=200, mimetype="application/json")

class AllDietGoals(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(AllDietGoals, self).__init__()
    def get(self):
        self.reqparse.add_argument('userid', type = str, required = True,
            location = 'headers')
        args= self.reqparse.parse_args()
        diet_goal = DietGoal(user_id=args['userid'])
        return diet_goal.get_user_goals_list(), 200
