#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe


@app.before_request
def check_if_logged_in():
    open_endpoint = ["signup", "login", "check_session"]
    if request.endpoint not in open_endpoint and not session.get("user_id"):
        return {"error": "Unauthorized"}, 401


class Signup(Resource):
    def post(self):

        data = request.get_json()
        password = data.get("password")

        user = User(
            username=data.get("username"),
            image_url=data.get("image_url"),
            bio=data.get("bio"),
        )

        user.password_hash = password
        try:
            db.session.add(user)
            # import ipdb; ipdb.set_trace()
            User.query.delete()
            db.session.commit()
            
            session["user_id"] = user.id

            return user.to_dict(), 201

        except Exception as e:
            return {"message": str(e)}, 422


class CheckSession(Resource):
    pass


class Login(Resource):
    pass


class Logout(Resource):
    pass


class RecipeIndex(Resource):
    pass


api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(RecipeIndex, "/recipes", endpoint="recipes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
