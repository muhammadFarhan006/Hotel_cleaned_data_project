import pandas as pd
import numpy as np
import re


#  Loading the dataset
df = pd.read_csv("hotel_bookings.csv")

#  Droping duplicates
df = df.drop_duplicates(keep="first")

#  Replace dirty placeholder text with NaN
dirty_values = ["?", "N/A", "None", "missing", ""]
df = df.replace(dirty_values, np.nan)

#  Handle Missing Values

##  Fill missing 'agent' values with median (data asymmetric)
if pd.api.types.is_numeric_dtype(df["agent"]):
    df["agent"] = df["agent"].fillna(df["agent"].median())

##  Fill missing 'company' values with mean (data symmetric)
if pd.api.types.is_numeric_dtype(df["company"]):
    df["company"] = df["company"].fillna(df["company"].mean())
else:
    df["company"] = df["company"].fillna("Unknown")

##  Fill missing 'children' values with median
if pd.api.types.is_numeric_dtype(df["children"]):
    df["children"] = df["children"].fillna(df["children"].median())

##  Randomly assign missing countries from existing ones
existing_countries = df["country"].dropna().unique()
df["country"] = df["country"].apply(
    lambda x: np.random.choice(existing_countries) if pd.isna(x) else x
)


#   Rename Columns
df = df.rename(columns={
    "is_canceled": "canceled",
    "arrival_date_year": "arrival_year",
    "arrival_date_month": "arrival_month",
    "required_car_parking_spaces": "parking_spaces",
    "total_of_special_requests": "special_requests",
    "reservation_status_date": "reservation_date",
    "arrival_date_week_number": "arrival_week",
    "days_in_waiting_list": "waiting_list",
    "is_repeated_guest": "repeated_guest",
    "stays_in_week_nights": "week_nights_stays",
    "arrival_date_day_of_month": "date_of_month",
    "previous_bookings_not_canceled": "bookings_not_canceled",
    "previous_cancellations": "bookings_canceled",
    "stays_in_weekend_nights": "weekend_nights_stays"
})

#   Format Text Columns (strip, lowercase, replace spaces/hyphens)
text_cols = df.select_dtypes(include="object").columns
df[text_cols] = df[text_cols].apply(lambda col:
    col.str.strip()
       .str.lower()
       .str.replace(" ", "_", regex=False)
       .str.replace("-", "_", regex=False)
)

#   Cleaning Specific Categorical Columns

##  Market Segment column
df["market_segment"] = df["market_segment"].replace({
    "online_ta": "online",
    "ofline_ta": "offline",
    "offline_ta/to": "offline",
    "undefined": np.nan,
    "complementary": np.nan
})
df["market_segment"] = df["market_segment"].fillna("offline")

##  Meal Column
df["meal"] = df["meal"].replace("undefined", "bb")

##  Distribution Channel column
df["distribution_channel"] = df["distribution_channel"].replace({
    "ta/to": "travel_agent",
    "undefined": "direct"
})


#  Formating Reservation Date
df["reservation_date"] = df["reservation_date"].astype(str).str.replace("_", "-", regex=False)
df["reservation_date"] = pd.to_datetime(df["reservation_date"], errors="coerce")

#  Final Summary
print(df.isna().sum())

#  Save Cleaned Dataset
df.to_excel("hotel_bookings_cleaned.xlsx", index=False)




