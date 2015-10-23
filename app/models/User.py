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

class User(Model):
    def __init__(self):
        super(User, self).__init__()
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
    def create(self, user_info):
        email_query = "SELECT email FROM users WHERE email = %s"
        email_data = [user_info['email']]
        email = self.db.query_db(email_query, email_data)

        errors = []
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        
        if not user_info['first_name']:
            errors.append('First name cannot be blank')
        elif not user_info['first_name'].isalpha():
            errors.append('First name cannot contain numbers')
        elif len(user_info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')

        if not user_info['last_name']:
            errors.append('Last name cannot be blank')
        elif not user_info['last_name'].isalpha():
            errors.append('Last name cannot contain numbers')
        elif len(user_info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')

        if not user_info['email']:
            errors.append('E-mail cannot be blank')
        elif len(user_info['email']) < 2:
            errors.append('E-mail must be at least 2 characters long')
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append('E-mail is not valid')
        if email:
            errors.append('E-mail already registered')

        if not user_info['password']:
            errors.append('Password cannot be blank')
        elif not user_info['password_confirmation']:
            errors.append('Password confirmation cannot be blank')
        elif len(user_info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user_info['password'] != user_info['password_confirmation']:
            errors.append('Passwords must match')

        if not user_info['dob']:
            errors.append('Date of birth cannot be blank')

        if not user_info['gender']:
            errors.append('Gender cannot be blank')

        if not user_info['feet']:
            errors.append('Height cannot be blank')

        if not user_info['weight']:
            errors.append('Weight cannot be blank')

        if not user_info['activity']:
            errors.append('Activity cannot be blank')

        if errors:
            return {'status': False, 'errors': errors}

        height = (int(user_info['feet']) * 12) + int(user_info['inches'])   #convert feet and inches from html form to be stored to database and used in calculation of calorie threshold       
        
        today = date.today() # this section is to calculate the user's approx. age
        year = today.year
        born_year = int((str(user_info['dob']))[0:4]) 
        age = year - born_year

        if len(user_info['activity']) == 3: # for activity level
            activity_level = 1.2
        elif len(user_info['activity']) == 4:
            activity_level = 1.725
        else: 
            activity_level = 1.55

        if len(user_info['gender']) == 4: # different formulas to calculate threshold depending on gender
            calorie_threshold = 66.47 + (13.75 * int(user_info['weight'])) + (5 * height) - (6.75 * age) # need function to calculate age from dob
        else:
            calorie_threshold = 665.09 + (9.56 * int(user_info['weight'])) + (1.84 * height) - (4.67 * age)
                 
        hashed_pw = self.bcrypt.generate_password_hash(user_info['password'])
        insert_query = "INSERT INTO users (first, last, email, password, created_at, updated_at, dob, gender, height, weight, activity, calories_threshold) VALUES (%s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)"
        insert_data = [user_info['first_name'], user_info['last_name'], user_info['email'], hashed_pw, user_info['dob'], user_info['gender'], height, user_info['weight'], user_info['activity'], calorie_threshold]
        self.db.query_db(insert_query, insert_data)
        get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
        user = self.db.query_db(get_user_query)

        insert_weight_query = "INSERT INTO weight (weight, created_at, updated_at, users_id) VALUES (%s, NOW(), NOW(), %s)" # section to enter weight into database (to store weight history)
        weight_data = [user[0]['weight'], user[0]['id']]
        self.db.query_db(insert_weight_query, weight_data)

        return {'status': True, 'user': user[0]}

    def login(self, user_info):
        login_query = "SELECT * FROM users WHERE email = %s"
        login_data = [user_info['email']]
        user = self.db.query_db(login_query, login_data)
        if user and self.bcrypt.check_password_hash(user[0]['password'], user_info['password']):
            return {'status': True, 'user': user[0]}
        else:
            return {'status': False}

    def user_info(self, id):
        all_users_query = "SELECT * FROM users WHERE id = %s"
        user_id = [id]
        return self.db.query_db(all_users_query, user_id)
