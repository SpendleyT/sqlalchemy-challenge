# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
from pathlib import Path

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify, request

#Constants Definition (from notebook)
BASE_START_DATE = '2016-08-23'
BUSIEST_STATION = 'USC00519281'

#################################################
# Database Setup
#################################################
## Get DB engine and connection
db_path = Path('./Resources/hawaii.sqlite')
engine = create_engine(f'sqlite:///{db_path}')

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Station = Base.classes.station
Measures = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Home page route
@app.route('/')
def home():
    return(f'Welcome to Hawaii Weather API Service.</br>'
           f'Available API calls:</br>'
           f'Precipitation by date (last 12 months): '
           f'<a href="http://127.0.0.1:5000/api/v1.0/precipitation">/api/v1.0/precipitation</a></br>'
           f'Stations list:  <a href="http://127.0.0.1:5000/api/v1.0/stations">/api/v1.0/stations</a></br>'
           f'Temperatures (last 12 months):  '
           f'<a href="http://127.0.0.1:5000/api/v1.0/tobs">/api/v1.0/tobs</a></br>'
           f'Temperatures since selected date:  /api/v1.0/range/:start_date (dates as YYYY-MM-DD)</br>'
           f'Temperatures between selected dates:  /api/v1.0/range/:start_date/:end_date (dates as YYYY-MM-DD)</br>'
        )

#get past 12 month date and precipitation amounts
@app.route('/api/v1.0/precipitation', methods=['GET'])
def get_precipitation():
    records = []
    results = session.query(Measures.station, Measures.date, Measures.prcp).where(Measures.date >= BASE_START_DATE)
    for row in results:
        records.append({
            "station": row.station, 
            "date": row.date, 
            "precipitation": row.prcp
        })
    return jsonify(records)

#get station list
@app.route('/api/v1.0/stations', methods=['GET'])
def get_stations():
    records = []
    results = session.query(Station).all()
    for row in results:
        records.append({
                "station": row.station, 
                "name": row.name, 
                "latitude": row.latitude,
                "longitude": row.longitude,
                "elevation": row.elevation
             })
    return jsonify(records)

#get past 12 months dates and temps for last year
@app.route('/api/v1.0/tobs', methods=['GET'])
def get_temps():
    records = [{"station": 'USC00519281'}]
    results = session.query(
        Measures.date, 
        func.min(Measures.tobs).label('min'), 
        func.max(Measures.tobs).label('max'), 
        func.avg(Measures.tobs).label('avg')
    ).where(Measures.station == BUSIEST_STATION).\
        where(Measures.date >= BASE_START_DATE).\
        group_by(Measures.date).all()
    for row in results:
        records.append({
            "date": row.date, 
            "min_temp": row.min, 
            "max_temp": row.max, 
            "avg_temp": row.avg
        })
    return jsonify(records)

#get min, max and avg temps since <start> date
@app.route('/api/v1.0/range/<start>', methods=['GET'])
def get_temp_from(start):
    records = [{"station": BUSIEST_STATION}]
    results = session.query(
        Measures.date, 
        func.min(Measures.tobs).label('min'), 
        func.max(Measures.tobs).label('max'), 
        func.avg(Measures.tobs).label('avg')
    ).where(Measures.date >= BASE_START_DATE).\
        where(Measures.station == BUSIEST_STATION).\
        group_by(Measures.date).all()
    for row in results:
        records.append({"date": row.date, "min_temp": row.min, "max_temp": row.max, "avg_temp": row.avg})
    return jsonify(records)

#get min, max and avg temps between <start> and <end>
@app.route('/api/v1.0/range/<start>/<end>', methods=['GET'])
def get_temp_between(start, end):
    records = [{"station": BUSIEST_STATION}]
    results = session.query(
        Measures.date, 
        func.min(Measures.tobs).label('min'), 
        func.max(Measures.tobs).label('max'), 
        func.avg(Measures.tobs).label('avg')
    ).filter(and_(Measures.date <= end, Measures.date >= BASE_START_DATE)).\
        where(Measures.station == BUSIEST_STATION).\
        group_by(Measures.date).all()
    for row in results:
        records.append({
            "date": row.date, 
            "min_temp": row.min, 
            "max_temp": row.max, 
            "avg_temp": row.avg
        })
    return jsonify(records)


if __name__ == '__main__':
    app.run(debug=True)