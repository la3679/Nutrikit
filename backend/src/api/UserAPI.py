import json
from flask import Response, request
from flask_restful import Resource
try:
    from db.UserRepository import UserRepository
    from model.User import User
except ImportError:
    from src.db.UserRepository import UserRepository
    from src.model.User import User

class UserAPI(Resource):
    def get(self, id: str):
        user = UserRepository.get_by_id(id)
        json_data = {}
        for key, value in user.__dict__.items():
            if key.find("_User__") != -1:
                continue
            json_data[key] = value
        return Response(json.dumps(json_data), status=200, mimetype="application/json")

    def put(self, id):
        request_body = request.get_json()
        user=UserRepository.get_by_id(id)
        user.email=request_body.get("email")
        user.display_name=request_body.get("display_name")
        user.height=request_body.get("height")
        user.weight=request_body.get("weight")
        user.set_password(request_body.get("password"))
        UserRepository.update(user)
        user = UserRepository.get_by_id(id)
        json_data = {}
        for key, value in user.__dict__.items():
            if key.find("_User__") != -1:
                continue
            json_data[key] = value
        return Response(json.dumps(json_data), status=200, mimetype="application/json")

    def delete(self, id):
        user=UserRepository.get_by_id(id)
        return UserRepository.delete(user)

class UsersAPI(Resource):
    def get(self):
        users = UserRepository.get_all()
        json_data = []
        for user in users:
            temp = {}
            for key, value in user.__dict__.items():
                if key.find("_User__") != -1:
                    continue
                temp[key] = value
            json_data.append(temp)
        return Response(json.dumps(json_data), status=200, mimetype="application/json")

    def post(self):
        request_body = request.get_json()
        id=request_body["id"]
        user = User(
            id=request_body["id"],
            display_name=request_body["display_name"],
            email=request_body["email"],
            height=request_body.get("height"),
            weight=request_body.get("weight"),
            password=request_body["password"]
        )
        UserRepository.create(user)
        user = UserRepository.get_by_id(id)
        json_data = {}
        for key, value in user.__dict__.items():
            if key.find("_User__") != -1:
                continue
            json_data[key] = value
        return Response(json.dumps(json_data), status=200, mimetype="application/json")

class AuthAPI(Resource):
    def post(self, action):
        if action == "login":
            request_body = request.get_json()
            id = request_body["id"]
            password = request_body["password"]
            user = UserRepository.get_by_id(id)
            if user is None:
                return Response(json.dumps({
                    "message": "User not found.",
                    "type": "ERROR"
                }), status=404, mimetype='application/json')
            if user.match_password(password):
                session_key = user.create_session_key()
                UserRepository.update(user)
                return Response(json.dumps({
                    "message": "User logged in successfully.",
                    "type": "INFO",
                    "access_token": session_key
                }), status=200, mimetype="application/json")
            else:
                return Response(json.dumps({
                    "message": "Incorrect password.",
                    "type": "INFO",
                }), status=403, mimetype="application/json")
        elif action == "logout":
            request_body = request.get_json()
            id = request_body.get("id")
            user = UserRepository.get_by_id(id)
            if user is None:
                return Response(json.dumps({
                    "message": "User not found.",
                    "type": "ERROR"
                }), status=404, mimetype="application/json")
            user.reset_session_key()
            UserRepository.update(user)
            return Response(json.dumps({
                "message": "User logged out successfully.",
                "type": "INFO"
            }), status=200, mimetype="application/json")
        elif action == "check_session":
            request_body = request.get_json()
            id = request_body["id"]
            access_token = request_body.get("access_token")
            user = UserRepository.get_by_id(id)
            return Response(json.dumps({
                "session_active": user.match_session_key(access_token),
                "type": "INFO"
            }), status=200, mimetype="application/json")
        else:
            return Response(json.dumps({
                "message": "Invalid action for auth.",
                "type": "ERROR"
            }), status=404, mimetype='application/json')