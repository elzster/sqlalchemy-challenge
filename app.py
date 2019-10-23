#app.py for Homework #10
#http://127.0.0.1:5000/

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request, render_template

###############################################
# Database Setup
###############################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

################################################
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
sun = "https://s3.amazonaws.com/zenplannerwordpress-stack0/wp-content/uploads/sites/479/2019/05/29130237/sunshine-sun-clip-art-with-transparent-background-free-sun-clipart-2361_2358-300x300.png"
station_link = "http://127.0.0.1:5000/api/v1.0/stations"
salad = "https://vignette.wikia.nocookie.net/fantheories/images/2/2c/Salad-Fingers-Episode-4--Salad-Fingers--Cage.jpg/revision/latest?cb=20140508224616"
precipitation_link = "http://127.0.0.1:5000/api/v1.0/precipitation"
tobs_link = "http://127.0.0.1:5000/api/v1.0/tobs"
start_link = "http://127.0.0.1:5000/api/v1.0/2017-01-01"
start_end_link = "http://127.0.0.1:5000/api/v1.0/2016-01-01/2017-01-01"

#HomePage Route
@app.route("/")
def home():
    return (
        f"<center><h1>Welcome to the Home Page!</h1></center><br>"
        f"<center><img src={salad}></center><br>"
        f"<center><b>Here are the available Routes:</b></center><br>"
        f"<center><a href={precipitation_link}> Precipitation</a></center><br>"
        f"<center><a href={station_link}>Stations</a></center><br>"
        f"<center><a href={tobs_link}>Observed Temperatures For Previous Year</a></center><br>"
        f"<center><a href={start_link}>Temperature on Specific Date</a></center><br>"
        f"<center><a href={start_end_link}>Temperature observed in specific range.</center>"
    )
#precipitation Results.
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    results2 = session.query(Measurement.date, Measurement.prcp).all()

    precip_list = []
    
    for x in results2:
        list_dict = {}
        list_dict['Date'] = x.date
        list_dict['Rainfall Amount'] = x.prcp
        precip_list.append(list_dict)
    
        session.close()
        
    return jsonify(precip_list)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    all_stations = []
    for x in results:
        list_dict = {}
        list_dict['Station No.'] = x.station
        list_dict['Station Location'] = x.name
        list_dict['Latitude'] = x.latitude
        list_dict['Longitude'] = x.longitude
        list_dict['Elevation'] = x.elevation
        all_stations.append(list_dict)
    
    
        session.close()

    return jsonify(all_stations)


# Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    results = session.query(Measurement.station, Station.name, Measurement.date, Measurement.tobs).\
                            filter(Measurement.station == Station.station).\
                            filter(Measurement.date >= '2016-08-24').\
                            filter(Measurement.date <= '2017-08-23').\
                            order_by(Measurement.date).all()
    
    #creates a dictionary to parse into json from results on merged tables.    
    tobs_list = []
    for x in results:
        list_dict = {}
        list_dict['Name'] = x.name
        list_dict['Date'] = x.date
        list_dict['Temp_Observed'] = x.tobs
        tobs_list.append(list_dict)

    
        session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/<date>")
def temperatures_date(date):

    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= date ).all()
    
#Query Using Date, Default entered is 2017-01-01
    temperatures = []
    for x in results:
        list_dict = {}
        list_dict['min'] = results[0][0]
        list_dict['avg'] = round(results[0][1],2)
        list_dict['max'] = results[0][2]
        temperatures.append(list_dict)


        session.close()
#this prints up a prettier webpage with some text display.
    return(
        f"<center><img src={sun}></center><br>"    
        f"<center><h3>Here are the temperature stats for {date}:</h3></center><br>"    
        f"<center>The Min Temperature was {list_dict['min']} degrees.</center><br>"
        f"<center>The Average Temperature was {list_dict['avg']} degrees.</center><br>"
        f"<center>The Max Temperature was {list_dict['max']} degrees.</center>"
    )


@app.route("/api/v1.0/<start>/<end>")
def temperatures_start(start, end):

    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start ).\
                filter(Measurement.date <= end ).all()
    
    # Convert list of tuples into normal list
#     # temperatures = list(np.ravel(results))

    # return jsonify(temperatures)
    temperatures = []
    for x in results:
        list_dict = {}
        list_dict['min'] = results[0][0]
        list_dict['avg'] = round(results[0][1],2)
        list_dict['max'] = results[0][2]
        temperatures.append(list_dict)


        session.close()

    return(
        f"<center><img src={sun}></center><br>"    
        f"<center><h3>Here are the temperature stats between {start} and {end}:</h3></center><br>"    
        f"<center>The Min Temperature was {list_dict['min']} degrees.</center><br>"
        f"<center>The Average Temperature was {list_dict['avg']} degrees.</center><br>"
        f"<center>The Max Temperature was {list_dict['max']} degrees.</center>"
    )


#this is to actively run flask server.
if __name__ == "__main__":
    app.run(debug=True)
    