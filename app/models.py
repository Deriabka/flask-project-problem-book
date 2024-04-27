import re
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


