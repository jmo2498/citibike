from google.cloud import bigquery
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


def query_trip_volume(lat, lon, temperature_f, distance_threshold=300.0, temp_tolerance=5.0) -> pd.DataFrame:
    client = bigquery.Client()

    min_temp = temperature_f - temp_tolerance
    max_temp = temperature_f + temp_tolerance

    query = f'''
    WITH time_buckets AS (
      SELECT
        DATE(starttime) AS trip_date,
        CASE
          WHEN EXTRACT(HOUR FROM starttime) < 12 THEN 'morning'
          WHEN EXTRACT(HOUR FROM starttime) < 18 THEN 'afternoon'
          ELSE 'evening'
        END AS time_bucket,
        COUNT(*) AS trip_count
      FROM `vertextraining-448821.trip_data.trip_data`
      WHERE
        ST_DISTANCE(
          ST_GEOGPOINT(start_station_longitude, start_station_latitude),
          ST_GEOGPOINT({lon}, {lat})
        ) < {distance_threshold}
        AND start_station_latitude IS NOT NULL
        AND start_station_longitude IS NOT NULL
        AND DATE(starttime) BETWEEN '2014-01-01' AND '2018-05-31'
      GROUP BY trip_date, time_bucket
    ),
    joined_with_weather AS (
      SELECT
        t.trip_date,
        t.time_bucket,
        t.trip_count,
        w.temperature,
        w.wind_speed,
        w.precipitation
      FROM time_buckets t
      JOIN `vertextraining-448821.weather_data_manhattan.laguardia_2014_2018` w
        ON t.trip_date = DATE(w.timestamp)
      WHERE w.temperature BETWEEN {min_temp} AND {max_temp}
    )
    SELECT *
    FROM joined_with_weather
    ORDER BY trip_date DESC, time_bucket
    LIMIT 300
    '''

    job = client.query(query)
    return job.to_dataframe().to_dict(orient="records") 
