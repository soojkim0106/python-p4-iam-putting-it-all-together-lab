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
        return {"error": "401: Unauthorized"}, 401


class Signup(Resource):
    def post(self):

        data = request.get_json()
        password = data.get("password")

        new_user = User(
            username=data.get("username"),
            image_url=data.get("image_url"),
            bio=data.get("bio"),
        )

        new_user.password_hash = password
        try:
            db.session.add(new_user)
            db.session.commit()
            
            session["user_id"] = new_user.id

            return new_user.to_dict(), 201

        except Exception as e:
            return {"message": str(e)}, 422


class CheckSession(Resource):
    def get(self):
        
        if user_id := session.get('user_id'):
            user = db.session.get(User, user_id)
            return user.to_dict(), 200

        return {},  401


class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            username = data.get('username')
            password = data.get('password')
            
            if user := User.query.filter(User.username == username).first():
                if user.authenticate(password):
                    session['user_id'] = user.id
                    return user.to_dict(), 200
            return {'error': 'Wrong username or password'}, 401
        except Exception as e:
            return {"error": str(e)}, 401

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        
        return {}, 204


class RecipeIndex(Resource):
    def get(self):
        
        user = User.query.filter(User.id == session['user_id']).first()
        
        return [recipe.to_dict() for recipe in user.recipes], 200
    
    def post(self):
        
        try:
            data = request.get_json()
            
            new_recipe = Recipe(**data)
            import ipdb; ipdb.set_trace()
            new_recipe.user_id = session.get("user_id")
            db.session.add(new_recipe)
            db.session.commit()
            
            return new_recipe.to_dict(), 201
        
        except Exception as e:
            return {"error": str(e)}, 422


api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session", endpoint="check_session")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(RecipeIndex, "/recipes", endpoint="recipes")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
