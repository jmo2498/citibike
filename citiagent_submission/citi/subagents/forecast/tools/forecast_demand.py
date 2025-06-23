import pandas as pd
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings
from statsmodels.tools.sm_exceptions import ValueWarning

warnings.filterwarnings("ignore", category=ValueWarning)


def forecast_demand(trip_df: pd.DataFrame, bucket: str = None) -> float:
    """
    Forecast the next time bucket's trip demand using Holt-Winters.

    Args:
        trip_df (pd.DataFrame): Trip data with 'trip_date', 'trip_count', and 'time_bucket'.
        bucket (str, optional): One of 'morning', 'afternoon', 'evening'.

    Returns:
        float: Forecasted trip count (rounded).
    """
    try:
        # Auto-select next time bucket based on current time
        if not bucket:
            hour = datetime.now().hour
            if hour < 12:
                bucket = "afternoon"
            elif hour < 17:
                bucket = "evening"
            else:
                bucket = "morning"

        # Filter to desired time bucket
        bucket_df = trip_df[trip_df["time_bucket"] == bucket].copy()
        if bucket_df.empty or len(bucket_df) < 10:
            return 0.0

        # Convert to proper datetime index and sort
        bucket_df["trip_date"] = pd.to_datetime(bucket_df["trip_date"])
        bucket_df = bucket_df.sort_values("trip_date")

        # Create time series
        series = bucket_df.set_index("trip_date")["trip_count"].dropna()

        # Fit Holt-Winters model
        model = ExponentialSmoothing(series, trend='add', seasonal=None)
        fit = model.fit()

        # Forecast next time step
        forecast = fit.forecast(1).iloc[0]
        return round(float(forecast), 1)

    except Exception as e:
        print(f"⚠️ Forecasting error: {e}")
        return 0.0