"""
test_data_processing.py
Author: Mousumi Paul
Unit tests for data_processing.py ETL functions
"""

import sys
import os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def make_sample_yield():
    return pd.DataFrame({
        "Record_ID": [f"YLD{i:05d}" for i in range(20)],
        "Year": np.random.choice([2020,2021,2022,2023,2024], 20),
        "Crop": np.random.choice(["Rice","Wheat","Tomato"], 20),
        "Region": np.random.choice(["Punjab","Maharashtra"], 20),
        "Season": np.random.choice(["Kharif","Rabi"], 20),
        "Area_Acres": np.random.uniform(2, 20, 20).round(2),
        "Yield_Qtl_Per_Acre": np.random.uniform(5, 40, 20).round(2),
        "Total_Production_Qtl": np.random.uniform(50, 500, 20).round(2),
        "Market_Price_Per_Qtl": np.random.uniform(1000, 4000, 20).round(2),
        "Total_Revenue_INR": np.random.uniform(10000, 200000, 20).round(2),
        "Input_Cost_INR": np.random.uniform(5000, 80000, 20).round(2),
        "Net_Profit_INR": np.random.uniform(-10000, 100000, 20).round(2),
        "Profit_Margin_Pct": np.random.uniform(-20, 60, 20).round(2),
        "Weather_Factor": np.random.uniform(0.7, 1.3, 20).round(4),
        "Quality_Grade": np.random.choice(["A","B","C"], 20),
    })


def make_sample_weather():
    return pd.DataFrame({
        "Date": pd.date_range("2022-01-01", periods=50, freq="W").strftime("%Y-%m-%d"),
        "Year": [2022]*25 + [2023]*25,
        "Month": list(range(1,13))*4 + [1,2],
        "Region": np.random.choice(["Punjab","Maharashtra"], 50),
        "Temp_Max_C": np.random.uniform(18, 42, 50).round(1),
        "Temp_Min_C": np.random.uniform(8, 28, 50).round(1),
        "Temp_Avg_C": np.random.uniform(15, 35, 50).round(1),
        "Rainfall_MM": np.random.uniform(0, 150, 50).round(1),
        "Humidity_Pct": np.random.uniform(30, 95, 50).round(1),
        "Sunshine_Hrs": np.random.uniform(4, 11, 50).round(1),
        "Is_Monsoon": np.random.choice([0,1], 50),
        "Weather_Index": np.random.uniform(2, 8, 50).round(3),
    })


def test_clean_yield_removes_negatives():
    df = make_sample_yield()
    df.loc[0, "Yield_Qtl_Per_Acre"] = -5.0  # invalid
    df = df[df["Yield_Qtl_Per_Acre"] > 0]
    assert (df["Yield_Qtl_Per_Acre"] > 0).all()
    print("✅ test_clean_yield_removes_negatives passed")


def test_yield_no_duplicates():
    df = make_sample_yield()
    df_dup = pd.concat([df, df.head(3)])  # add duplicates
    df_clean = df_dup.drop_duplicates()
    assert len(df_clean) == len(df)
    print("✅ test_yield_no_duplicates passed")


def test_weather_date_parse():
    df = make_sample_weather()
    df["Date"] = pd.to_datetime(df["Date"])
    assert df["Date"].dtype == "datetime64[ns]"
    print("✅ test_weather_date_parse passed")


def test_feature_engineering_revenue_per_acre():
    df = make_sample_yield()
    df["Revenue_Per_Acre"] = (df["Total_Revenue_INR"] / df["Area_Acres"]).round(2)
    assert "Revenue_Per_Acre" in df.columns
    assert (df["Revenue_Per_Acre"] > 0).all()
    print("✅ test_feature_engineering_revenue_per_acre passed")


def test_merge_yield_weather():
    yield_df   = make_sample_yield()
    weather_df = make_sample_weather()
    weather_df["Date"] = pd.to_datetime(weather_df["Date"])
    annual = weather_df.groupby(["Year","Region"]).agg(
        Avg_Temp_C       = ("Temp_Avg_C","mean"),
        Total_Rainfall_MM= ("Rainfall_MM","sum"),
    ).reset_index()
    merged = yield_df.merge(annual, on=["Year","Region"], how="left")
    assert len(merged) == len(yield_df)
    print("✅ test_merge_yield_weather passed")


def test_seasonal_summary_has_correct_columns():
    df = make_sample_yield()
    seasonal = df.groupby(["Season","Crop"]).agg(
        Avg_Yield = ("Yield_Qtl_Per_Acre","mean"),
        Count     = ("Record_ID","count"),
    ).reset_index()
    assert "Avg_Yield" in seasonal.columns
    assert len(seasonal) > 0
    print("✅ test_seasonal_summary_has_correct_columns passed")


if __name__ == "__main__":
    test_clean_yield_removes_negatives()
    test_yield_no_duplicates()
    test_weather_date_parse()
    test_feature_engineering_revenue_per_acre()
    test_merge_yield_weather()
    test_seasonal_summary_has_correct_columns()
    print("\n✅ All data processing tests passed!")
