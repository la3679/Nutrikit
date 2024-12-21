from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from api.ItemAPI import ItemsAPI, ItemAPI
from api.UserAPI import UserAPI, UsersAPI, AuthAPI
from api.DietGoal import DietGoalManagement, AllDietGoals
from api.DietTracker import DietTrackerManagement
from api.DietPlanAPI import DietPlan

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# user accounts api
api.add_resource(UserAPI, '/users/<string:id>')
api.add_resource(UsersAPI, '/users')
api.add_resource(AuthAPI, '/auth/<string:action>')

api.add_resource(ItemAPI, '/items/<int:id>')
api.add_resource(ItemsAPI, '/items')

# to be decided
# food items/meal items will be handled using single type items
# api.add_resource(FoodItem, '/fooditems')
# api.add_resource(MealItem, '/mealitems')
# api.add_resource(FoodCategories, '/foodcategory')

api.add_resource(DietGoalManagement, '/diet')
api.add_resource(DietPlan, '/dietplan')


api.add_resource(AllDietGoals, '/diet/all')

api.add_resource(DietTrackerManagement, '/tracker')

if __name__ == '__main__':
    app.run(debug=True)