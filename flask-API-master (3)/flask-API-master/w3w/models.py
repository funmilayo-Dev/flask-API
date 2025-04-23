from sqlalchemy import Date, Time, Integer, Float
from w3w import ma
from w3w import db

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

class Observer(db.Model):
    date = db.Column(Date, primary_key=True)
    time = db.Column(Time, nullable=False)
    timezone_offset = db.Column(Integer, nullable=False)
    coordinates = db.Column(Float, nullable=False)
    temperature_land_surface = db.Column(db.String(80), nullable=False)
    temperature_sea_surface = db.Column(db.Integer, nullable=False)
    humidity = db.Column(Integer, nullable=False)
    wind_direction = db.Column(Integer, nullable=False)
    wind_speed = db.Column(Integer, nullable=False)
    precipitation = db.Column(Integer, nullable=False)
    haze = db.Column(Integer, nullable=False)

    def __repr__(self):
        return 'date %r' % self.date
    
class ObserverSchema(ma.SQLAlchemyAutoSchema):
    """definition used by serialization library based on observers model"""
    class Meta:
        fields = ("long", "lat", "date", "time", "timezone_offset", "coordinates",
                  "temperature_land_surface", "temperature_sea_surface", "humidity", 
                  "wind_direction", "wind_speed", "precipitation", "haze")

observer_schema = ObserverSchema()
observers_schema = ObserverSchema(many=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f"<location {self.lat}, {self.long}: {self.address}>"
    
    