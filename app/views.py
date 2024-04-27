from app import app,USERS,models
from flask import request,Response
import json
from http import HTTPStatus

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.post('/create/user')
def create_user():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]
    if not(models.User.validate_email(email)) or not(models.User.validate_phone(phone)):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(id,first_name,last_name,phone,email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "score": user.score
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )
    return response
@app.get('/users/<int:user_id>')
def get_user(user_id):
    if user_id<0 or user_id>=len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "score": user.score
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )
    return response

