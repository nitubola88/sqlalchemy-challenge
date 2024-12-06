# Module 10: SQLAlchemy Challenge 

# Climate Analysis and Flask API with SQLAlchemy

## Overview
This project is part of the Bootcamp Module 10 Challenge, where I performed a climate analysis and designed a Flask API based on the provided dataset. The analysis involves using Python, SQLAlchemy ORM queries, Pandas, and Matplotlib to explore climate data. Additionally, a Flask API is designed to serve the analyzed data through various routes.

## SQLAlchemy Connection
- Used `create_engine()` to connect to the SQLite database.
- Used `automap_base()` to reflect tables into classes (`station` and `measurement`).
- Created a session to link Python to the database.

## Precipitation Analysis
- Identified the most recent date in the dataset.08/23/2017
- Queried the previous 12 months of precipitation data.
- Loaded and visualized data using Pandas and Matplotlib.
- Printed summary statistics for the precipitation data.
- mean        0.177279
- std         0.461190,indicating significant variability
- Min/Max Precipitation: Rainfall ranged from 0.0 inches (dry days) to 6.7 inches (heavy rainfall).
- We can plan trip to avoid the wettest months (typically winter or monsoon seasons in tropical climates).Understanding that rainfall can be intense (with some very heavy days) will help us pack appropriately.
  Best Time to Visit should be during drier months based on precipitation patterns to avoid rainy periods.


## Station Analysis
- Calculated the total number of stations.9
- Found the most active station.'USC00519281'that is Wakiki,Honolulu
- Computed lowest, highest, and average temperatures for the most active station.(54.0, 85.0, 71.66378066378067)
- Obtained the previous 12 months of TOBS data for the most active station.
- Plotted a histogram of TOBS.
-  With average temperatures around 71.66°F and a moderate range between 54°F and 85°F, Wakiki,Honolulu experiences a comfortable climate most of the time. This makes it an excellent vacation destination since you don’t need to worry about extreme temperatures.The temperatures are mild, so you likely won't need heavy winter clothes

## Flask API Routes
- **`/`**: Homepage with available routes.
- **`/api/v1.0/precipitation`**: Precipitation data for the last 12 months.
- **`/api/v1.0/stations`**: List of all stations.
- **`/api/v1.0/tobs`**: TOBS data for the most active station in the last year.
- **`/api/v1.0/<start>`**: Min, avg, and max temperatures from a specified start date to the end.
- **`/api/v1.0/<start>/<end>`**: Min, avg, and max temperatures for a specified date range.

## Code Source
The code source can be found here: [GitHub Repository](https://github.com/nitubola88/sqlalchemy-challenge.git)
