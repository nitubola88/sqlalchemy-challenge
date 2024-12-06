# Import the dependencies.

from sqlalchemy import create_engine, Date, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from datetime import datetime as dt  # Import datetime module
from collections import OrderedDict


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement=Base.classes.measurement
Station=Base.classes.station


# Create our session (link) from Python to the DB
Session = Session(bind=engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# Define routes
@app.route('/')
def home():
    return( 
            f"Welcome to thr Hawaii climate Analysis API!<br/><br/>" 
            f"Available routes<br/><br/>"
            f"'/api/v1.0/precipitation', 'Get precipitation data'<br/>" 
            f"'/api/v1.0/stations', 'List all stations'<br/>"
            f"'/api/v1.0/tobs', 'Get temperature observations for the most active station'<br/>"
            f"'/api/v1.0/&lt;start&gt;', 'Get min, avg, max temperatures from start date (YYYY-MM-DD)'<br/>"
            f"'/api/v1.0/&lt;start&gt;/&lt;end&gt;', 'Get min, avg, max temperatures between start and end dates (YYYY-MM-DD)'<br/>"
        )
 



@app.route('/api/v1.0/precipitation')
def precipitation():
     # Query precipitation data for the last 12 months
    results = precipitation_data = Session.query(
    Measurement.date,
    Measurement.prcp
).filter(
    Measurement.date >= func.date(Session.query(func.max(Measurement.date)).scalar(), '-1 year')  # Use max date - 1 year
).all()
     # Convert the results to a dictionary with date as key and prcp as value
    precipitation_data = [
        {"date": result.date, "prcp": result.prcp} for result in results
    ]
    return jsonify(precipitation_data)



@app.route('/api/v1.0/stations')
def stations():
    # Query all distinct stations 
    results = Session.query(Station.station).distinct().all()
   
    # Prepare the data in a list of dictionaries
    station_data = [{"station": result[0]} for result in results] # result is a tuple
    
    # Return the JSONified data
    return jsonify(station_data)



@app.route('/api/v1.0/tobs')
def tobs():
    # Get the most active station
    most_active_station = Session.query(Measurement.station,func.count(Measurement.station).label('count')).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    if most_active_station:
        # Assuming we have a Station model to get the station name
        station_id = most_active_station[0]
        # get station name corresponding to station id
        station_name = Session.query(Station.name).filter(Station.station == station_id).scalar()
       
        
       # Query the dates and TOBS for the previous year for the most active station
        results = Session.query(Measurement.date, Measurement.tobs).filter(
                Measurement.station == station_id,
                Measurement.date >= (Session.query(func.date(func.max(Measurement.date), '-1 year')).scalar())).all()

        # Format the results into a list of dictionaries
        tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]
        # Sort the TOBS data by date 
        tobs_data.sort(key=lambda x: x['date'])  # Sort by date

        # Get the observation count for the previous year
        observation_count = len(tobs_data)

        
        return jsonify ({
            "station_id": station_id,
            "station_name": station_name,
            "observation_count": observation_count,
            "tobs_data": tobs_data,
            
        
         })
    else:
        return jsonify({"error": "No temperature observations found."}), 404


@app.route('/api/v1.0/<start>')
def start_date(start):
    # Convert start date from string to datetime
    try:
        start_date = dt.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Query for min, avg, max temperatures from start date
    results = Session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

    return jsonify({
        "Start Date": start_date,
        "Min Temperature": results[0][0],
        "Avg Temperature": results[0][1],
        "Max Temperature": results[0][2]
    })




@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    # Convert start and end dates from string to datetime
    try:
        start_date = dt.strptime(start, '%Y-%m-%d')
        end_date = dt.strptime(end, '%Y-%m-%d')
        if not start_date or not end_date:
           return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 
 # Query the database for min, avg, and max temperatures within the date range
        stats = Session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.avg(Measurement.tobs).label('avg_temp'),
        func.max(Measurement.tobs).label('max_temp')
         ).filter(Measurement.date >= start_date,Measurement.date <= end_date).one()

        # Return the results as JSON
        return jsonify({
            "start_date": start_date,
            "end_date": end_date,
            "min_temperature": stats.min_temp,
            "avg_temperature": stats.avg_temp,
            "max_temperature": stats.max_temp
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)