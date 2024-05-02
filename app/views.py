from app import app,USERS,models,EXPRES,QUESTS
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
    if not models.User.is_valid_id(user_id):
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
            "string_expression": expr.to_string(),
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )
    return response

@app.get('/math/<int:expression_id>')
def get_expression(expression_id):
    if not models.Expression.is_valid_id(expression_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    expr = EXPRES[expression_id]
    response = Response(
        json.dumps({
            "id": expr.id,
            "operation": expr.operation,
            "values": expr.values,
            "string_expression": expr.to_string(),
        }),
        HTTPStatus.OK,
        mimetype="application/json")
    return response

@app.post('/math/<int:expression_id>/solve')
def get_solve(expression_id):
    data = request.get_json()
    if not models.Expression.is_valid_id(expression_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    expr = EXPRES[expression_id]
    user_id = data["user_id"]
    user_answer = data["user_answer"]
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    if expr.answer == user_answer:
        user.increase_score(expr.reward)
    response = Response(
        json.dumps({
            "expression_id": expression_id,
            "result": 'Верный' if expr.answer == user_answer else 'Неверный',
            "reward": expr.reward
        }),
        HTTPStatus.OK,
        mimetype="application/json")
    return response


@app.post("/questions/create")
def questions_create():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    question_type = data["type"]
    question_id = len(QUESTS)
    if question_type == "ONE-ANSWER":
        answer = data["answer"]
        if not models.OneQuestion.is_valid(answer):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.OneQuestion(question_id, title, description, answer, reward=1)
        QUESTS.append(question)
        return Response(
            json.dumps(
                {
                    "id": question.id,
                    "title": question.title,
                    "description": question.description,
                    "type": question_type,
                    "answer": question.answer
                }
            ),
            status=HTTPStatus.OK,
            mimetype="application/json")
    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]  # list
        answer = data["answer"]  # int
        if not models.MoreQuestions.is_valid(answer, choices):
            return Response(status=HTTPStatus.BAD_REQUEST)
        question = models.MoreQuestions(question_id, title, description, answer, choices, reward=1)
        QUESTS.append(question)
        return Response(
            json.dumps(
                {
                    "id": question.id,
                    "title": question.title,
                    "description": question.description,
                    "type": question_type,
                    "choices": question.choices,
                    "answer": question.answer
                }
            ),
            status=HTTPStatus.CREATED,
            mimetype="application/json")