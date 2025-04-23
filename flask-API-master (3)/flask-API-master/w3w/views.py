#from app import app
from w3w import db
from w3w.models import User, users_schema, user_schema, Observer, observers_schema, observer_schema, Location
from flask import jsonify, request, Blueprint, json
import jwt, datetime
import what3words
from functools import wraps

api = Blueprint('api', __name__) # url_prefix='/api' add for context 
#view = Blueprint('views', __name__) url_prefix='/api' <- for context

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, api.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'invalid token'})
        
        return f( *args , **kwargs)
    return decorator

@api.get('/')
def hello_world():
    """endpoint used for testing purposes"""
    return "<h1> Hello World <h1>" #{"hello":"world"}

@api.post("/login")
def login():
    """endpoint used for authentication"""
    auth = request.authorization
    # to check if basic auth values are present
    if auth:
        # check if username and password are correct
        if auth.username == "Emmanuel" and auth.password == "APIPassword":
             token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.now() + datetime.timedelta(minutes = 30)},
                                 api.config ['SECRET_KEY'])
                          
             return {"token": token}
        else:
            return {"message": "error - username or password incorrect"}, 401
    else:
        return {"message": "no authorisation details"}, 401       

@api.get('/users/get-all-users')
@token_required
def get_all_users():
    """endpoint used to view all users records"""
    users = User.query.all()
    return users_schema.jsonify(users)

@api.get('/users/get-one-user/<user_id>')
@token_required
def get_one_user_route(user_id): # user_id is accepted as arg
    """endpoint uses route parameters to determine user to be queried"""
    user = User.query.filter_by(user_id=user_id).first()
    return user_schema.jsonify(user)

@api.get('/users/get-one-user')
@token_required
def get_one_user_query():
    """endpoint uses query params to determine student to be queried"""
    user_id = request.args.get('user_id') # req.args.get() used to access query params
    user = User.query.filter_by(user_id=user_id).first()
    return user_schema.jsonify(user)

@api.get('/users/get-one-user-json')
@token_required
def get_one_user_json():
    """endpoint uses json to determine user to be queried"""
    json_data = request.get_json() # req.get_json() is used to access json data
    print(json_data) # used for debugging purposes 
    user_id = json_data['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    return user_schema.jsonify(user)

@api.post("/users/add-user-json")
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

@api.delete('/users/delete-one-user/<user_id>')
@token_required
def delete_one_user_route(user_id): # user id is accepted as argument
    """endpoint uses path parameters to determine user to be removed from db"""
    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return {"User deleted": f"user_id: {user_id}"}

@api.put("/users/update-user")
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


@api.get('/get-coordinates')
def get_address_by_coordinates():
    latitude = request.args.get('latitude')
    longitude = request.arg.get('longitude')

    location = Location.query.filter_by(latitude=latitude, longitude=longitude).first()
    if location:
        return jsonify({'address': location.address}), 200
    else:
        return jsonify({'error': 'Location not found'}), 404

# Getting obervations from what3words
@api.get('/get-word-address')
def get_address():
    latitude = request.args.get('lat')
    longitude = request.args.get('long')

    # convert coordinates to 3-word address
    address = address.convert_to_3wa(what3words.Coordinates(51.484463, -0.195405))

    if address:
        new_location = Location(latitude=latitude, longitude=longitude, address=address)
        db.session.add(new_location)
        db.session.commit()
        return jsonify({'address': address}), 200
    else:
        return jsonify({'error': 'Failed to retrieve address'}), 500
    
@api.get('/get-coordinates')
def get_coordinates(latitude, longitude):
    
    # to convert 3-word address to cordinates
    coordinates = coordinates.convert_to_coordinates('prom.cape.pump')
    params = {
        "coordinates": f"{latitude}, {longitude}",
        "key": "V2QAXYTL"
    }

    # response = requests.get(url, params=params)
    # if response.status_code == 200:
    #     data = response.json
    #     return data.get('words')
    # else:
    #     return None

    # To convert to coordinates
    latitude = latitude.convert_to_coordinates('prom.cape.pump')
    longitude = longitude.convert_to_coordinates('prom.cape.pump')

# POSTing weather obervations from user
# (Get all observations)
@api.get('/observations')
def get_observations():
    all_observations = Observer.query.all()
    result = observers_schema.dump(all_observations)
    return jsonify(result)

# Create
@api.post('/api/observation')
def add_observation():
    json_data = request.get_json()
    print(json_data)

    new_observation = Observer (
        date = json_data['date'],
        time = json_data['time'],
        timezone_offset = json_data['tz_offset'],
        coordinates = json_data['coordinatess'],
        temperature_land_surface = json_data['tmp_land'],
        temperature_sea_surface = json_data['tmp_sea'],
        humidity = json_data['humidity'],
        wind_direction = json_data['wind_dir'],
        wind_speed = json_data['wind_speed'],
        precipitation = json_data['precipitation'],
        haze = json_data['haze']
    )
    db.session.add(new_observation)
    db.session.commit()
    print("Observation added")
    print(json.dumps(json_data, indent=4)) # used for debugging purposes

    # try:
    #     new_observation = Observer(**data)
    #     db.session.add(new_observation)
    #     db.session.commit()
    #     return observer_schema.jsonify(new_observation), 201
    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({"message": "Observation already exists"}), 409
    
    return observer_schema.jsonify(new_observation)
    
    # Read route (Get single observation)
@api.get('/observation/<date>')
def get_observation(date):
    observation = Observer.query.get(date)
    if observation:
        return observer_schema.jsonify(observation)
    else:
        return jsonify({"message": "Observation not found"}), 404

    # Update route
@api.put('/observation/<date>')
def update_observation(date):
    observation = Observer.query.get(date)
    if observation:
        data = request.json
        for key, value in data.items():
            setattr(observation, key, value)
        db.session.commit()
        return observer_schema.jsonify(observation)
    else:
        return jsonify({"message": "Observation not found"}), 404
    
    # Delete route
@api.delete('/observation/<date>')
def delete_observation(date):
    observation = Observer.query.get(date)
    if observation:
        db.session.delete(observation)
        db.session.commit()
        return jsonify({"message": "Observation deleted successfully"})
    else:
        return jsonify({"message": "Observation not found"}), 404