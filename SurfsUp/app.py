#import dependencies
import numpy as np

import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup for database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Create a home page 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Climate Analysis and Exploration Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>Dictionary of date and precipitation<br/><br/>"
        f"/api/v1.0/stations<br/>List of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Dictionary of date and tobs of the most active station for the last year of the data<br/><br/>"
        f"/api/v1.0/<start_date_only><br/>Min, max, avg tobs for all dates greater than and equal to the start date.<br/><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>Min, max, avg tobs for dates between the start and end date inclusive.<br/><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create session from Python
    session = Session(engine)

    # Query date and prcp for the last 12 months
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    #create dictionary for data and prcp
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations (): #ask for stations
    session = Session(engine)

    result = session.query(Station.station).all()

    session.close()

    #create a list of stations
    station_list = []
    for station in result:
        station_list.append(station)

    return jsonify(station_list)
    

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Query dates and temperature observations 
    Result =  session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Station.station == Measurement.station).filter(Station.name == 'WAIHEE 837.5, HI US').all()

    session.close()

    #temperature observations
    tobs_list = []
    for date, tobs in Result:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs 
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start_date_only>")
def StartDate(start_date_only):
    session = Session(engine)
    Results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date_only).group_by(Measurement.date).all()
    session.close()

    #list of max, min, avg tobs
    start_list = []
    for date,tmin,tmax,tavg in Results:
        start_dict = {}
        start_dict['Date'] = date
        start_dict['TMIN'] = tmin
        start_dict['TMAX'] = tmax
        start_dict['TAVG'] = tavg
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def StartDateEndDate(start_date,end_date):
    session = Session(engine)
    Results1 = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date<=end_date).group_by(Measurement.date).all()
    session.close()
    startend_list = []
    for date,Tmin,Tmax,Tavg in Results1:
        startend_dict = {}
        startend_dict['Date'] = date
        startend_dict['TMIN'] = Tmin
        startend_dict['TMAX'] = Tmax
        startend_dict['TAVG'] = Tavg
        startend_list.append(startend_dict)

    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)