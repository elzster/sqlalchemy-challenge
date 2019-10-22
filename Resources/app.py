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
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page!<br>"
        f"Here are the following Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return "This is the precipitation page."

@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()
    
    #SELECT name FROM passenger;
    
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)





@app.route("/api/v1.0/stations")
def stations():
    return "This is the stations page."

@app.route("/api/v1.0/tobs")
def temperature():
    return "This is the observed temperature page."

# List all routes that are available.

# /api/v1.0/precipitation

# Convert the query results to a Dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

# /api/v1.0/stations

# Return a JSON list of stations from the dataset.
# /api/v1.0/tobs

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# Hints
# You will need to join the station and measurement tables for some of the analysis queries.

# Use Flask jsonify to convert your API data into a valid JSON response object.
if __name__ == "__main__":
    app.run(debug=True)