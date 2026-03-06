"""
data_processing.py
Author: Mousumi Paul
ETL pipeline for AI Farm Dashboard
"""
import pandas as pd
import numpy as np
import os

def load_raw():
    base = "data/raw"
    return {
        "yield":   pd.read_csv(f"{base}/crop_yield_records.csv"),
        "weather": pd.read_csv(f"{base}/weather_data.csv"),
    }

def build_weather_annual(df):
    return df.groupby(["Year","Region"]).agg(
        Avg_Temp_C        = ("Avg_Temp_C","mean"),
        Total_Rainfall_MM = ("Rainfall_MM","sum"),
        Avg_Humidity_Pct  = ("Humidity_Pct","mean"),
        Avg_Sunshine_Hrs  = ("Sunshine_Hrs","mean"),
        Weather_Index_Avg = ("Weather_Score","mean"),
    ).round(2).reset_index()

def main():
    data = load_raw()
    # Rename yield columns to match downstream expectations
    yield_df = data["yield"].rename(columns={
        "Yield_Per_Acre_Qtl": "Yield_Qtl_Per_Acre",
        "Total_Yield_Qtl":    "Total_Production_Qtl",
        "Net_Profit_INR":     "Net_Profit_INR",
        "Market_Price_Per_Qtl": "Market_Price_Per_Qtl",
    })
    yield_df["Profit_Margin_Pct"] = (yield_df["Net_Profit_INR"] / yield_df["Total_Revenue_INR"] * 100).round(2)
    yield_df = yield_df.drop_duplicates()
    yield_df = yield_df[yield_df["Yield_Qtl_Per_Acre"] > 0].reset_index(drop=True)

    weather_annual = build_weather_annual(data["weather"])
    merged = yield_df.merge(weather_annual, on=["Year","Region"], how="left")
    merged["Revenue_Per_Acre"]     = (merged["Total_Revenue_INR"] / merged["Area_Acres"]).round(2)
    merged["Yield_Efficiency"]     = (merged["Yield_Qtl_Per_Acre"] / merged.groupby("Crop")["Yield_Qtl_Per_Acre"].transform("mean")).round(3)
    merged["Adequate_Rainfall"]    = (merged["Total_Rainfall_MM"].fillna(0) >= 600).astype(int)
    merged                         = merged.sort_values(["Crop","Region","Year"])
    merged["YoY_Yield_Change_Pct"] = merged.groupby(["Crop","Region"])["Yield_Qtl_Per_Acre"].pct_change().mul(100).round(2)

    os.makedirs("data/processed", exist_ok=True)
    merged.to_csv("data/processed/yield_weather_merged.csv", index=False)

    seasonal = merged.groupby(["Year","Season","Crop"]).agg(
        Avg_Yield        =("Yield_Qtl_Per_Acre","mean"),
        Total_Production =("Total_Production_Qtl","sum"),
        Avg_Revenue      =("Total_Revenue_INR","mean"),
        Avg_Profit       =("Net_Profit_INR","mean"),
        Avg_Margin_Pct   =("Profit_Margin_Pct","mean"),
    ).round(2).reset_index()
    seasonal.to_excel("data/processed/seasonal_summary.xlsx", index=False)

    print(f"✅ yield_weather_merged.csv → {len(merged)} rows × {merged.shape[1]} cols")
    print(f"✅ seasonal_summary.xlsx    → {len(seasonal)} rows")
    return merged

if __name__ == "__main__":
    main()
