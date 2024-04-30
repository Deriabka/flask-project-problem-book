from flask import Flask

app = Flask(__name__)

USERS = []
EXPRES = []

from app import views