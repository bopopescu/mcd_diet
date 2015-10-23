""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
from datetime import date

class Meal(Model):
    def __init__(self):
        super(Meal, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
    def add_meal(self, id, user_info):
        meal_check_query = "SELECT * FROM meals WHERE users_id = %s and created_date = CURDATE()"
        meal_check_data = [id]
        meal_check = self.db.query_db(meal_check_query, meal_check_data)

        if not meal_check:

            get_user_query = "SELECT * FROM users WHERE id = %s"
            user_id = [id]
            user = self.db.query_db(get_user_query, user_id)

            calorie_deficit = int(user_info['calories']) - int(user[0]['calories_threshold'])

            add_meal_query = "INSERT INTO meals (total_calories, created_at, updated_at, users_id, calorie_deficit, created_date) VALUES (%s, NOW(), NOW(), %s, %s, NOW())"
            add_meal_data = [user_info['calories'], id, calorie_deficit]
            self.db.query_db(add_meal_query, add_meal_data)
            return {'status': True, 'user': user[0]}

        else:
            errors = ['Error: Meals have already been added for the day']
            return {'status': False, 'errors': errors}

    def all_meals(self, id):
        get_all_meals_query = "SELECT * FROM meals WHERE users_id = %s"
        all_meals_data = [id]
        return self.db.query_db(get_all_meals_query, all_meals_data)



        
