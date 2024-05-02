from flask import Flask

app = Flask(__name__)

USERS = []
EXPRES = []
REVARD = 0
QUESTS = []

from app import views