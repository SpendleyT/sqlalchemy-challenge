# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
from pathlib import Path

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
## Get DB engine and connection
db_path = Path('/Resources/hawaii.sqlite')
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
@app.route('/')
def home():
    pass

#get past 12 month date and precipitation amounts
@app.route('/api/v1.0/precipitation')
def get_precipitation():
    pass

#get station list
@app.route('stations')
def get_stations():
    pass

#get past 12 months dates and temps for last year
@app.route('/api/v1.0/tobs')
def get_temps():
    pass

#get min, max and avg tempssince <start> date
@app.route('/api/v1.0/<start>')
def get_temp_from():
    pass

#get min, max and avg temps between <start> and <end>
@app.route('/api/v1.0/<start>/<end>')
def get_temp_between():
    pass


