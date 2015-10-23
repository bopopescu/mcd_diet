"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """
        self.load_model('User')
        self.load_model('Weight')
        self.load_model('Meal')

    """ This is an example of a controller method that will load a view for the client """
    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """
        return self.load_view('index.html')

    def register(self):
        return self.load_view('register.html')

    def success(self):
        id = session['id']
        users = self.models['User'].user_info(id)
        return self.load_view('/users/home.html', users = users)

    def submit(self):
        user_info = request.form
        result = self.models['User'].create(user_info)
        if result['status']:
            session['id'] = result['user']['id']
            session['first'] = result['user']['first']
            return redirect('/success')
        else:
            for message in result['errors']:
                flash(message)
            return redirect('/register')

    def login(self):
        user_info = request.form
        result = self.models['User'].login(user_info)
        if result['status'] is True:
            session['id'] = result['user']['id']
            session['first'] = result['user']['first']
            return redirect('/success')
        else:
            flash('Invalid E-mail or Password')
            return redirect('/')

    def logout(self):
        session.pop('id')
        session.pop('first')
        return redirect('/')

    def meals(self, id):
        meals = self.models['Meal'].all_meals(id)
        return self.load_view('/users/meals.html', meals = meals) 

    def add_meal(self, id):
        user_info = request.form
        result = self.models['Meal'].add_meal(id, user_info)
        if result['status']:
            return redirect('/menu/'+ id)
        else:
            for message in result['errors']:
                flash(message)
            return redirect('/menu/'+ id)

    def weight(self, id):
        weights = self.models['Weight'].user_weight(id)
        return self.load_view('/users/weight.html', weights = weights)

    def update_weight(self, id):
        user_info = request.form
        self.models['Weight'].update_weight(id, user_info)
        self.models['Weight'].update_calorie_threshold(id)
        return redirect('/weight/'+ id)

    def menu(self, id):
        users = self.models['User'].user_info(id)
        return self.load_view('/users/menu.html', users = users)


