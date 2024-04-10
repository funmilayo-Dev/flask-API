# Security techniques for REST API

# import Flask class def from library
from flask import Flask, request, jsonify
import json

# SQLAlchemy is an ORM allowimng decoupling of Db operations
from flask_sqlalchemy import SQLAlchemy
# MArshmallow is an obj serialization/deserialization library
from flask_marshmallow import Marshmallow

import jwt
import datetime

from functools import wraps

# instantiate app based off flask
app = Flask(__name__)

#app.app_context().push()

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db' #path to Db
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'EmmanuelAPISecretKey'

# instantiate db obj using the SQLAlchemy class with the Flask app obj as arg
db = SQLAlchemy(app)

# SQLAlchemy must be initialised before Flask-Marshmallow
ma = Marshmallow(app)

# class def for SQLALCHEMY ORM
class User(db.Model):
    """def of user model used by SQLAlchemy"""
    user_id = db.Column(db.String(80), primary_key=True)
    user_firstname = db.Column(db.String(80), nullable=False)
    user_surname = db.Column(db.String(80), nullable=False)
    user_company = db.Column(db.String(80), nullable=False)
    user_occupation = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_id

# class def for MArshmallow serialisation
class UserSchema(ma.SQLAlchemyAutoSchema):
    """def used by serialisation library based on user model"""
    class Meta:
        fields = ("user_id","user_firstname","user_surname","user_company","user_occupation","user_occupation","user_email")
  
# instantiate objs based on MArshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'invalid token'})
        
        return f( *args , **kwargs)
    return decorator

@app.get('/')
def hello_world():
    """endpoint used for testing purposes"""

    return {"hello":"world"}

@app.get("/login")
def login():
    """endpoint used for authentication"""
    auth = request.authorization
    # to check if basic auth values are present
    if auth:
        # check if username and password are correct
        if auth.username == "Emmanuel" and auth.password == "APIPassword":
             token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.now() + datetime.timedelta(minutes = 30)}, app.config ['SECRET_KEY'])
                          
             return {"token": token}
        else:
            return {"message": "error - username or password incorrect"}, 401
    else:
        return {"message": "no authorisation details"}, 401       

@app.get('/users/get-all-users')
@token_required
def get_all_users():
    """endpoint used to view all users records"""
    users = User.query.all()
    return users_schema.jsonify(users)

@app.get('/users/get-one-user/<user_id>')
@token_required
def get_one_user_route(user_id): # user_id is accepted as arg
    """endpoint uses route parameters to determine user to be queried"""
    user = User.query.filter_by(user_id=user_id).first()
    return user_schema.jsonify(user)

@app.get('/users/get-one-user')
@token_required
def get_one_user_query():
    """endpoint uses query params to determine student to be queried"""
    user_id = request.args.get('user_id') # req.args.get() used to access query params
    user = User.query.filter_by(user_id=user_id).first()
    return user_schema.jsonify(user)

@app.get('/users/get-one-user-json')
@token_required
def get_one_user_json():
    """endpoint uses json to determine user to be queried"""
    json_data = request.get_json() # req.get_json() is used to access json data
    print(json_data) # used for debugging purposes 
    user_id = json_data['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    return user_schema.jsonify(user)

@app.post("/users/add-user-json")
@token_required
def users_add_json():
    """endpoint uses json to add user record to db"""
    json_data = request.get_json() # req.get_json() used to access json sent
    print(json_data) # used for debugging purposes

    new_user = User (
        user_id = json_data['user_id'],
        user_firstname = json_data['user_firstname'],
        user_surname = json_data['user_surname'],
        user_company = json_data['user_company'],
        user_occupation = json_data['user_occupation'],
        user_email = json_data['user_email']
    )
    db.session.add(new_user)
    db.session.commit()
    print("Record added:")
    print(json.dumps(json_data, indent=4)) # used for debugging purposes
    
    return user_schema.jsonify(new_user)

@app.delete('/users/delete-one-user/<user_id>')
@token_required
def delete_one_user_route(user_id): # user id is accepted as argument
    """endpoint uses path parameters to determine user to be removed from db"""
    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return {"User deleted": f"user_id: {user_id}"}

@app.put("/users/update-user")
@token_required
def update_users_json():
    """endpoint uses json to update student record in db"""
    json_data = request.get_json() # req.get_json is used to access json sent 
    print(json.dumps(json_data, indent = 4)) # used for debugging purposes

    User.query.filter_by(user_id=json_data['user_id']).update(
        dict 
        (
            user_firstname = json_data['user_firstname'],
            user_surname = json_data['user_surname'],
            user_company = json_data['user_company'],
            user_occupation = json_data['user_occupation'],
            user_email = json_data['user_email']
        )
    )
    db.session.commit()
    return {"message": "User's record updated successfully"}

#hello_world()
if __name__ == '__main__':
    app.run()
