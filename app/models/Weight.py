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

class Weight(Model):
    def __init__(self):
        super(Weight, self).__init__()
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
    def update_weight(self, id, user_info):
        update_weight_query = "UPDATE users SET weight = %s WHERE id = %s" # to update weight in user table
        update_weight_data = [user_info['weight'], id]
        self.db.query_db(update_weight_query, update_weight_data)

        get_user_query = "SELECT * FROM users WHERE id = %s"
        user_id = [id]
        user = self.db.query_db(get_user_query, user_id)

        insert_weight_query = "INSERT INTO weight (weight, created_at, updated_at, users_id) VALUES (%s, NOW(), NOW(), %s)" # to store weight history)
        weight_data = [user[0]['weight'], user[0]['id']]
        self.db.query_db(insert_weight_query, weight_data)

    def user_weight(self, id):
        user_weight_query = "SELECT * FROM weight WHERE users_id = %s"
        user_weight_data = [id]
        return self.db.query_db(user_weight_query, user_weight_data)

    def update_calorie_threshold(self, id):
        get_user_query = "SELECT * FROM users WHERE id = %s"
        user_id = [id]
        user = self.db.query_db(get_user_query, user_id)

        today = date.today() # this section is to calculate the user's approx. age
        year = today.year
        born_year = int((str(user[0]['dob']))[0:4]) 
        age = year - born_year

        if len(user[0]['gender']) == 4: # different formulas to calculate threshold depending on gender
            calorie_threshold = 66.47 + (13.75 * int(user[0]['weight'])) + (5 * int(user[0]['height'])) - (6.75 * age) 
        else:
            calorie_threshold = 665.09 + (9.56 * int(user[0]['weight'])) + (1.84 * int(user[0]['height'])) - (4.67 * age)

        update_calorie_query = "UPDATE users SET calories_threshold = %s WHERE id = %s"
        update_calorie_data = [calorie_threshold, id]
        return self.db.query_db(update_calorie_query, update_calorie_data)

        
