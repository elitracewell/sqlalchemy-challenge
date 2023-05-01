# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a Flask app instance
app = Flask(__name__)

# define homepage route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    # calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # query the precipitation data for the last 12 months
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # create a dictionary from the query results and append to a list of all_results
    all_results = []
    for date, prcp in prcp_data:
        results_dict = {}
        results_dict[date] = prcp
        all_results.append(results_dict)

    # return the JSON representation of the list of dictionaries
    return jsonify(all_results)

# define stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations."""
    # query all stations
    stations = session.query(Station.station).all()

    # convert list of tuples into a normal list
    all_stations = list(np.ravel(stations))

    # return the JSON list of stations
    return jsonify(all_stations)

# define tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature data for the last 12 months for the most active station."""
    # calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # query the temperature observations for the most active station for the last 12 months
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count().desc()).first()[0]
    temp_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == most_active_station).\
                filter(Measurement.date >= year_ago).all()

    # create a dictionary from the query results and append to a list of all_results
    all_results = []
    for date, tobs in temp_data:
        results_dict = {}
        results_dict[date] = tobs
        all_results.append(results_dict)

    # return the JSON representation of the list of dictionaries
    return jsonify(all_results)