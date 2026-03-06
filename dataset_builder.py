"""
dataset_builder.py
Author: Mousumi Paul
Prepares and formats final datasets optimized for Power BI ingestion.
"""

import pandas as pd
import numpy as np
import json
import os


def build_powerbi_master(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Final dataset for Power BI. Adds computed columns that are easier
    to use in DAX than to compute in Power Query.
    """
    df = merged_df.copy()

    # Year as text for clean axis labels
    df["Year_Label"] = df["Year"].astype(str)

    # Profit status flag for conditional formatting
    df["Profit_Status"] = df["Net_Profit_INR"].apply(
        lambda x: "Profitable" if x > 0 else "Loss")

    # Yield band for histogram-style slicing
    df["Yield_Band"] = pd.cut(
        df["Yield_Qtl_Per_Acre"],
        bins=[0, 10, 20, 30, 40, 200],
        labels=["0–10","10–20","20–30","30–40","40+"]
    ).astype(str)

    # Rainfall band
    if "Total_Rainfall_MM" in df.columns:
        df["Rainfall_Band"] = pd.cut(
            df["Total_Rainfall_MM"].fillna(0),
            bins=[0, 400, 700, 1000, 1500, 9999],
            labels=["< 400","400–700","700–1000","1000–1500","1500+"]
        ).astype(str)

    # Season-Year for timeline axis
    df["Season_Year"] = df["Season"] + " " + df["Year_Label"]

    # Round floats for clean display
    float_cols = df.select_dtypes(include="float64").columns
    df[float_cols] = df[float_cols].round(2)

    return df


def build_weather_monthly_summary(weather_df: pd.DataFrame) -> pd.DataFrame:
    """Monthly weather aggregation for line charts in Power BI."""
    weather_df = weather_df.copy()
    weather_df["Date"] = pd.to_datetime(weather_df["Date"])
    return weather_df.groupby(["Year","Month","Region"]).agg(
        Avg_Temp_C       = ("Temp_Avg_C","mean"),
        Total_Rainfall_MM= ("Rainfall_MM","sum"),
        Avg_Humidity_Pct = ("Humidity_Pct","mean"),
        Avg_Sunshine_Hrs = ("Sunshine_Hrs","mean"),
        Weather_Index    = ("Weather_Index","mean"),
    ).round(2).reset_index()


def build_ai_insights_table(outputs_dir: str = "data/chatgpt_outputs") -> pd.DataFrame:
    """
    Load all ChatGPT JSON outputs into a flat table for embedding
    as a Power BI text card data source.
    """
    rows = []
    file_map = {
        "yield_insights.json":          "Yield Analysis",
        "weather_impact_summary.json":  "Weather Impact",
        "seasonal_recommendations.json":"Seasonal Advice",
    }
    for fname, category in file_map.items():
        path = os.path.join(outputs_dir, fname)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            data = json.load(f)
        for key, val in data.items():
            val_str = "; ".join(val) if isinstance(val, list) else (
                json.dumps(val) if isinstance(val, dict) else str(val))
            rows.append({
                "Category":  category,
                "Insight_Key": key.replace("_"," ").title(),
                "Insight_Value": val_str,
            })
    return pd.DataFrame(rows)


def build_crop_season_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: crop × season → avg yield. Used for heatmap in Power BI."""
    return df.pivot_table(
        index="Crop", columns="Season",
        values="Yield_Qtl_Per_Acre", aggfunc="mean"
    ).round(2).reset_index()


def save_powerbi_datasets(merged_df: pd.DataFrame,
                           weather_df: pd.DataFrame,
                           out_dir: str = "data/processed"):
    os.makedirs(out_dir, exist_ok=True)

    master = build_powerbi_master(merged_df)
    master.to_excel(f"{out_dir}/powerbi_master_dataset.xlsx", index=False)

    monthly = build_weather_monthly_summary(weather_df)
    monthly.to_excel(f"{out_dir}/powerbi_weather_monthly.xlsx", index=False)

    ai_table = build_ai_insights_table()
    if len(ai_table) > 0:
        ai_table.to_excel(f"{out_dir}/powerbi_ai_insights.xlsx", index=False)

    crop_matrix = build_crop_season_matrix(merged_df)
    crop_matrix.to_excel(f"{out_dir}/powerbi_crop_season_matrix.xlsx", index=False)

    print(f"✅ powerbi_master_dataset.xlsx     → {len(master)} rows")
    print(f"✅ powerbi_weather_monthly.xlsx    → {len(monthly)} rows")
    print(f"✅ powerbi_ai_insights.xlsx        → {len(ai_table)} rows")
    print(f"✅ powerbi_crop_season_matrix.xlsx → {len(crop_matrix)} rows")
