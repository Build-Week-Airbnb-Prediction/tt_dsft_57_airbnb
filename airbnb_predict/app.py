"""Main file for Airbnb Price Predictor."""

import json
import os
from os import getenv
from tempfile import mkdtemp
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from joblib import load
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from category_encoders import OrdinalEncoder
from sklearn.pipeline import make_pipeline
from .models import DB, Listing


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
        "DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    features = load_features()

    airbnb_model = load('forest_model_best.pkl')

    listing = {}

    @app.route('/', methods=["GET", "POST"])
    def predict_one():
        features = load_features()
        predict_message = "Enter your listing's details"
        if request.method == "POST":
            listing = get_input_data()

            features = update_default_features(listing)

            DB.session.add(Listing(id=randint(0, 100_000), **listing))
            DB.session.commit()
            
            predicted_rate = get_prediction(
                airbnb_model, transform_input_data(listing))
            predict_message = f"Your suggested price is ${predicted_rate:.2f}"

        return render_template('predict-one.html', title="Price Finder", forms=features, message=predict_message)

    @app.route('/add_listing', methods=["GET", "POST"])
    def add_listing():
        """Add a new listing to the database"""
        if request.method == "POST":
            listing = get_input_data()
        return render_template('listing.html', title="Add a Listing", forms=features, message=f"{listing}")

    @app.route('/predict', methods=["POST"])
    def predict():
        return render_template('predict.html', title='Home', message="Coming Soon")

    @app.route('/reset')
    def test_db():
        listing = {}
        DB.drop_all()
        DB.create_all()
        return "DB created"

    @app.route('/return-all')
    def return_db_entries():
        temp_db_query = Listing.query.all()
        list_of_listings = []
        for id in temp_db_query:
            list_of_listings.append(id)
        print("A" + str(list_of_listings))
        return render_template('return-all.html', title="List of Listings", listings=list_of_listings)

    return app


def load_features():
    feature_order = get_feature_orders()
    with open('features.json') as file:
        all_possible = json.load(file)
        features = {feature: all_possible[feature]
                    for feature in feature_order}
        return features
    

def get_feature_orders():
    feature_order = [
        "property_type",
        "room_type",
        "accommodates",
        "bedrooms",
        "baths",
        "beds",
        "availability_365",
        "minimum_nights",
        "maximum_nights",
        "price",
        "latitude",
        "longitude",
    ]
    return feature_order


def get_input_data():
    listing = {}
    features = load_features()
    data = request.form.to_dict(flat=False)
    for key, value in data.items():
        if features[key]['type'] == "number":
            listing[key] = float(value[0])
        elif features[key]['type'] == "latitude":
            listing[key] = int(value[0])
        else:
            listing[key] = value[0]

    return listing


def transform_input_data(data):
    return {key: [value] for key, value in data.items()}


def get_prediction(model, listing):
    try:
        data_types = {"cleaning_fee": bool, "instant_bookable": bool}
        df = (pd.DataFrame(listing).astype(data_types))[
            get_feature_orders()]
    except:
        df = pd.DataFrame(listing)[get_feature_orders()]

    return model.predict(df)[0]


def update_default_features(listing):
    with open('features.json', 'r') as file:
        data = json.load(file)
        data['accommodates']['default'] = listing['accommodates']
        data['bedrooms']['default'] = listing['bedrooms']
        data['baths']['default'] = listing['baths']
        data['beds']['default'] = listing['beds']
        data['property_type']['default'] = listing['property_type']
        data['availability_365']['default'] = listing['availability_365']
        data['minimum_nights']['default'] = listing['minimum_nights']
        data['maximum_nights']['default'] = listing['maximum_nights']
        data['price']['default'] = listing['price']
        data['latitude']['default'] = listing['latitude']
        data['longitude']['default'] = listing['longitude']
        

    with open('features.json', 'w+') as file:
        json.dump(data, file)

    return data

