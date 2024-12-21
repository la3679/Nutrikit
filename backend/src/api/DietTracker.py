import json
from flask import Response
from flask_restful import Resource, reqparse
try:
    from db.DietTracker import *
except ImportError:
    from src.db.DietTracker import *

class DietTrackerManagement(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(DietTrackerManagement).__init__()
    def get(self):
        self.reqparse.add_argument('userid', type = str, required = True,
            location = 'headers')
        args= self.reqparse.parse_args()
        diet_tracker = DietTracker(args['userid'])
        return diet_tracker.get_comsumption(), 200


    def post(self):
        self.reqparse.add_argument('user_id', type = str, required = True,
            location = 'json')
        self.reqparse.add_argument('item_id', type = int, required = True,
            location = 'json')
        self.reqparse.add_argument('amount', type = float, required = True,
            location = 'json')      
        args= self.reqparse.parse_args()
        diet_tracker = DietTracker(args['user_id'])
        return diet_tracker.add_consumed_item(args['item_id'],args['amount']), 201

    def put(self):
        self.reqparse.add_argument('user_id', type = str, required = True,
            location = 'json')
        self.reqparse.add_argument('entry_id', type = int, required = True,
            location = 'json')
        self.reqparse.add_argument('amount', type = float, required = True,
            location = 'json') 
        args= self.reqparse.parse_args()
        if(args['amount']<=0):
            return {'message':'Wrong amount'}, 400
        diet_tracker = DietTracker(args['user_id'])
        diet_tracker.modify_amount(args['entry_id'],args['amount'])
        return '', 204  

    def delete(self):
        self.reqparse.add_argument('user_id', type = str, required = True,
            location = 'args')
        self.reqparse.add_argument('entry_id', type = int, required = True,
            location = 'args')
        args= self.reqparse.parse_args()
        print(args)
        diet_tracker = DietTracker(args['user_id'])
        diet_tracker.delete_item(args['entry_id'])
        return Response(json.dumps({
            "message": "SUCCESS"
        }), status=200, mimetype="application/json")
