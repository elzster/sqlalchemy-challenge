#app.py for Homework #10
#http://127.0.0.1:5000/

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
################################################

app= Flask(__name__)

#################################################
# Flask Routes
#################################################
# Routes
# /
# Home page.
#Hyperlinks for Homepage.

station_link = "http://127.0.0.1:5000/api/v1.0/stations"
salad = "https://vignette.wikia.nocookie.net/fantheories/images/2/2c/Salad-Fingers-Episode-4--Salad-Fingers--Cage.jpg/revision/latest?cb=20140508224616"
precipitation_link = "http://127.0.0.1:5000/api/v1.0/precipitation"
tobs_link = "http://127.0.0.1:5000/api/v1.0/tobs"

@app.route("/")
def home():
    return (
        f"<h1>Welcome to the Home Page!</h1><br>"
        f"<img src={salad}><br>"
        f"<b>Here are the available Routes:</b><br>"
        f"<a href={precipitation_link}> Precipitation</a><br>"
        f"<a href={station_link}>Stations</a><br>"
        f"<a href={tobs_link}>Observed Temperatures</a><br>"
    )
#precipitation Results.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # return "This is the precipitation page." #<---Testing Paths
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results2 = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results2))

    return jsonify(all_precipitation)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
#Needs to return just a list of all stations.
@app.route("/api/v1.0/stations")
def stations():
    # return "This is the stations page."
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station, Station.name).all()

    session.close()

    #SELECT name FROM passenger;

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def temperature():
    return "This is the observed temperature page."

# List all routes that are available.

# /api/v1.0/precipitation

# Convert the query results to a Dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

#Will need this for returning a list dictionary as jSON.
# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# Hints
# You will need to join the station and measurement tables for some of the analysis queries.

# Use Flask jsonify to convert your API data into a valid JSON response object.
if __name__ == "__main__":
    app.run(debug=True)
