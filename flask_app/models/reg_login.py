from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re


class Registration:
    def __init__(self,data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO registration (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("registration_form").query_db(query,data)


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM registration WHERE email=%(email)s"
        user_db =  connectToMySQL("registration_form").query_db(query,data)

        if len(user_db) < 1:
            return False
        return cls(user_db[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM registration WHERE id=%(user_id)s"
        results = connectToMySQL("registration_form").query_db(query,data)
        return cls(results[0])
        


    @staticmethod
    def validate_reg(reg):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        is_valid = True
        if len(reg["first_name"]) < 2:
            flash ("Please enter first name")
            is_valid = False

        if len(reg["last_name"]) < 2:
            flash ("Please enter last name")
            is_valid = False

        if not email_reg.match(reg["email"]): 
            flash("Invalid email address")
            is_valid = False

        else:
            query = "SELECT * FROM registration WHERE email = %(email)s;"
            data = {
                    "email": request.form["email"]
                }
            result = connectToMySQL("registration_form").query_db(query, data)
            if len(result) > 0:
                flash("Email is already taken")
                is_valid = False

        if len(reg["password"]) < 8:
            flash ("Password must incluse atleast 8 characters")
            is_valid = False

        if reg['confirm_password'] != reg['password']:
            flash("Passwords must match")
            is_valid = False

        return is_valid

