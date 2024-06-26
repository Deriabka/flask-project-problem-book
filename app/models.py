import re
from app import USERS,EXPRES
from abc import ABC,abstractmethod
class User:
    def __init__(self,id,first_name,last_name,phone,email,score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score

    @staticmethod
    def validate_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def validate_phone(phone):
        if re.match(r"^\+?[1-9][0-9]{7,14}$",phone):
            return True
        return False

    @staticmethod
    def is_valid_id(user_id):
        if user_id<0 or user_id>=len(USERS):
            return False
        return True

    def increase_score(self,amount=1):
        self.score += amount

class Expression:
    def __init__(self,id,operation,*values,reward=None):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()
        if reward is None:
            reward = len(values)-1
        self.reward = reward


    def __evaluate(self):
        return eval(self.to_string())

    def to_string(self):
        expr_str = (str(self.values[0]) + ''.join(f' {self.operation} {value}' for value in self.values[1:]))
        return expr_str
    @staticmethod
    def is_valid_id(expr_id):
        if expr_id<0 or expr_id>=len(EXPRES):
            return False
        return True

class Questions(ABC):
    def __init__(self, id, title, description, reward=None):
        self.id = id
        self.title = title
        self.description = description
        if reward is None:
            reward = 1
        self.reward = reward
        self._answer = None
    @property
    @abstractmethod
    def answer(self):
        pass

class OneQuestion(Questions):
    def __init__(self, id, title, description, answer:str, reward=None):
        super().__init__(id,title,description,reward)
        if self.is_valid(answer):
            self._answer = answer
        else:
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, new_answer:str):
        if self.is_valid(new_answer):
            self._answer = new_answer

    @staticmethod
    def is_valid(answer):
        return isinstance(answer, str)

class MoreQuestions(Questions):
    def __init__(self, id, title, description, answer:int, choices:list, reward=None):
        super().__init__(id,title,description,reward)
        if self.is_valid(answer,choices):
            self.choices = choices
            self._answer = answer
        else:
            self.choices = None
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self,new_answer):
        if self.is_valid(new_answer,self.choices):
            self._answer = new_answer

    @staticmethod
    def is_valid(answer,choices):
        if not isinstance(answer,int) or not isinstance(choices,list):
            return False
        if answer<0 and answer>=len(choices):
            return False
        return True











