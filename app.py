#import dependencies
from flask import Flask, jsonify

import numpy as np

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

import datetime as dt 

#reflect tables into ORM
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
#references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#impliment flask
app = Flask(__name__)

#routes
@app.route('/')
def home():
    """available routes:"""
    return(
        f"Available API Routes: <br/>"
        f"/precipitation/<date> <br/>"
        f"/stations <br/>"
        f"/tobs"
    )

@app.route("/precipitation/<date>")
def prec(date):
    """
    return dictionary (jsonified) for provided date
    """
    result = {date: session.query(Measurement.date == date).all()}
    return(jsonfiy(result))

@app.route('/stations')
def stations():
    """
    return list of stations
    """
    result = session.query(Station.station, Station.name,\
                            Station.latitude, Station.longitude,\
                            Station.elevation).all()
    return(jsonfiy(result))

@app.route('/tobs')
def tobs():
    """
    return last year of date (jsonified)
    """
    #find last date
    last_date = session.query(Measurement.date).\
                                order_by(Measurement.date.desc()).\
                                first()
    last_date = dt.datetime.strptime(last_date.date, '%Y-%m-%d')
    #find year before last date
    yr_ago = last_date - dt.timedelta(days = 365)

    last_yr_data = session.query(Measurement.date, Measurement.prcp).\
                                filter(Measurement.date >= yr_ago).all()
    return(jsonify(last_yr_data))


if __name__ == '__main__':
    app.run(debug=True)