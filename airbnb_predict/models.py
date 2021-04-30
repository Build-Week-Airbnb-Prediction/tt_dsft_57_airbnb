"""SQLAlchemy models for Airbnb"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Listing(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    property_type = DB.Column(DB.String, nullable=False)
    room_type = DB.Column(DB.String, nullable=False)
    accommodates = DB.Column(DB.Integer, nullable=False)
    bedrooms = DB.Column(DB.Integer, nullable=False)
    baths = DB.Column(DB.Numeric, nullable=False)
    beds = DB.Column(DB.Numeric, nullable=False)
    minimum_nights = DB.Column(DB.Integer, nullable=False)
    maximum_nights = DB.Column(DB.Integer, nullable=False)
    availability_365 = DB.Column(DB.Integer, nullable=False)
    price = DB.Column(DB.Integer, nullable=False)
    latitude = DB.Column(DB.Float, nullable=False)
    longitude = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        rep = f"""Id: {self.id} Property Type: {self.property_type} Room Type: {self.room_type} Accommodates: {self.accommodates} Bedrooms: {self.bedrooms} Baths: {self.baths} Zip: {self.zip}"""
        return rep
