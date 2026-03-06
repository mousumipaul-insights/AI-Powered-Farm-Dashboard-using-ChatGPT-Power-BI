# Data Dictionary — AI Farm Dashboard
**Author:** Mousumi Paul

## crop_yield_records.csv
| Column | Type | Description |
|--------|------|-------------|
| Record_ID | string | Unique ID |
| Year | int | Harvest year 2020-2024 |
| Month | int | Month 1-12 |
| Season | string | Kharif/Rabi/Zaid |
| Crop | string | Crop type |
| Variety | string | Seed variety |
| Region | string | Geographic region |
| Area_Acres | float | Cultivated area |
| Yield_Per_Acre_Qtl | float | Quintals per acre |
| Total_Yield_Qtl | float | Total output |
| Cost_Per_Acre_INR | float | Input cost per acre |
| Market_Price_Per_Qtl | float | Mandi selling price |
| Total_Revenue_INR | float | Total revenue |
| Net_Profit_INR | float | Revenue minus cost |

**Derived:** Profit_Margin_Pct, ROI_Pct, Month_Name, Year_Season

## weather_data.csv
| Column | Type | Description |
|--------|------|-------------|
| Rainfall_MM | float | Monthly rainfall |
| Max/Min/Avg_Temp_C | float | Temperature range |
| Humidity_Pct | float | Relative humidity |
| Weather_Score | float | Composite 0-1 score |
| Drought_Flag | int | 1 = rainfall < 20mm |
| Flood_Risk_Flag | int | 1 = rainfall > 300mm |

## AI Output Fields (crop_summaries.json)
| Field | Description |
|-------|-------------|
| ai_summary | Full GPT-generated text |
| dashboard_text | Truncated version for Power BI card |
| sentiment | Positive / Neutral / Negative |
| avg_yield | Numeric yield statistic |
| top_region | Best-performing region |
