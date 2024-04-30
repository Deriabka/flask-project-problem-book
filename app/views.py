from app import app,USERS,models,EXPRES
from flask import request,Response
import json
from http import HTTPStatus
import random

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.post('/create/user')
def create_user():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]
    if not(models.User.validate_email(email)) or not(models.User.validate_phone(phone)):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id,first_name,last_name,phone,email)
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

@app.get('/math/expression')
def generate_expression():
    data = request.get_json()
    expr_id = len(EXPRES)
    count_nums = data["count_nums"]
    operation = data["operation"] # +,-,//,*,**
    if operation == "random":
        operation = random.choice(["+","-","*","//","**"])
    min_expr = data["min"]
    max_expr = data["max"]
    values = [random.randint(min_expr,max_expr) for _ in range(count_nums)]
    if count_nums<2 or (operation not in {'+','*'} and count_nums>2):
        return Response(status=HTTPStatus.BAD_REQUEST)
    expr = models.Expression(expr_id,operation,*values)
    EXPRES.append(expr)
    response = Response(
        json.dumps({
            "id": expr.id,
            "operation": expr.operation,
            "values": expr.values,
            "string_expression": expr.to_string()
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )
    return response

@app.get('/math/<int:expression_id>')
def get_expression(expression_id):
    if expression_id<0 or expression_id>=len(EXPRES):
        return Response(status=HTTPStatus.NOT_FOUND)
    expr = EXPRES[expression_id]
    response = Response(
        json.dumps({
            "id": expr.id,
            "operation": expr.operation,
            "values": expr.values,
            "string_expression": expr.to_string()
        }),
        HTTPStatus.OK,
        mimetype="application/json")
    return response