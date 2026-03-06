# 📊 Power BI Dashboard Setup Guide
**Author:** Mousumi Paul — AI-Powered Farm Dashboard

---

## 1. Prerequisites
- Power BI Desktop (free download from microsoft.com/power-bi)
- Python pipeline completed: `python scripts/run_pipeline.py`
- Data files present in `data/processed/`

---

## 2. Connecting Data Sources

### Step A — Open Power BI Desktop
Open `farm_dashboard.pbix` from this folder.

### Step B — Update Data Source Paths
1. Go to **Home → Transform Data → Data Source Settings**
2. For each source, click **Change Source** and update to your local path:

| Source File | Purpose |
|-------------|---------|
| `powerbi_master_dataset.xlsx` | Primary data — yield + weather merged |
| `powerbi_weather_monthly.xlsx` | Monthly weather trends |
| `powerbi_ai_insights.xlsx` | ChatGPT insights table |
| `powerbi_crop_season_matrix.xlsx` | Crop × season heatmap |
| `seasonal_summary.xlsx` | Seasonal aggregated stats |

### Step C — Apply Custom Theme
1. Go to **View → Themes → Browse for Themes**
2. Select `theme/farm_theme.json`
3. Click **Apply**

### Step D — Refresh Data
Click **Home → Refresh** to load the latest data.

---

## 3. Dashboard Page Descriptions

### Page 1: 🏠 Overview
**Purpose:** Executive summary — one-glance view of farm performance.

| Visual | Type | Data Field |
|--------|------|-----------|
| Total Records | KPI Card | COUNT(Record_ID) |
| Avg Yield (Qtl/Acre) | KPI Card | AVERAGE(Yield_Qtl_Per_Acre) |
| Avg Profit Margin | KPI Card | AVERAGE(Profit_Margin_Pct) |
| AI Trend Direction | Text Card | yield_insights → trend_direction |
| Top Crop | KPI Card | MAX yield crop |
| Yield by Crop | Horizontal Bar | Crop vs Avg Yield |

---

### Page 2: 📈 Yield Trends
**Purpose:** How yield has changed year-over-year across crops and regions.

| Visual | Type | Data Fields |
|--------|------|------------|
| Yield Over Time | Line Chart | Year vs Avg_Yield (per Crop) |
| Yield by Region | Map / Bar | Region vs Avg_Yield |
| Yield Distribution | Box Plot | Yield_Qtl_Per_Acre by Crop |
| YoY Change % | Column Chart | Year vs YoY_Yield_Change_Pct |

**Slicers:** Crop, Region, Year, Quality_Grade

---

### Page 3: 🌦️ Weather Impact
**Purpose:** Understand how rainfall and temperature affect yields.

| Visual | Type | Data Fields |
|--------|------|------------|
| Rainfall vs Yield | Scatter Plot | Total_Rainfall_MM vs Yield_Qtl_Per_Acre |
| Temperature Trend | Line Chart | Month vs Avg_Temp_C |
| Monthly Rainfall | Bar Chart | Month vs Total_Rainfall_MM |
| Weather Index | Line | Year vs Weather_Index_Avg |

**Key DAX Measure:**
```
Rainfall_Yield_Correlation =
CALCULATE(
    CORR(yield_weather[Total_Rainfall_MM], yield_weather[Yield_Qtl_Per_Acre])
)
```

---

### Page 4: 📅 Seasonal Patterns
**Purpose:** Compare Kharif vs Rabi vs Zaid performance.

| Visual | Type | Data Fields |
|--------|------|------------|
| Season Comparison | Grouped Bar | Season vs Avg_Yield, Avg_Profit |
| Calendar Heatmap | Matrix | Month vs Region, color = Yield |
| Top Crops per Season | Table | Season → Crop ranked |
| Seasonal Revenue | Area Chart | Season_Year vs Total_Revenue |

---

### Page 5: 🤖 AI Insights
**Purpose:** Display ChatGPT analysis results as readable text cards.

| Visual | Type | Source |
|--------|------|--------|
| Yield Trend Summary | Text Card | AI Insights table, Category = "Yield Analysis" |
| Weather Impact | Text Card | AI Insights table, Category = "Weather Impact" |
| Seasonal Advice | Text Card | AI Insights table, Category = "Seasonal Advice" |
| Crop Comparison | Multi-row Card | Crop_Comparison_Report.txt |
| AI Recommendations | Bullet list | key_findings from yield_insights.json |

---

## 4. Key DAX Measures to Create

```DAX
-- Average Yield
Avg Yield = AVERAGE(powerbi_master[Yield_Qtl_Per_Acre])

-- Profit Margin %
Avg Margin % = AVERAGE(powerbi_master[Profit_Margin_Pct])

-- YoY Yield Growth
YoY Growth % =
VAR CurrentYear = MAX(powerbi_master[Year])
VAR LastYear = CurrentYear - 1
RETURN
DIVIDE(
    CALCULATE(AVERAGE(powerbi_master[Yield_Qtl_Per_Acre]), powerbi_master[Year] = CurrentYear) -
    CALCULATE(AVERAGE(powerbi_master[Yield_Qtl_Per_Acre]), powerbi_master[Year] = LastYear),
    CALCULATE(AVERAGE(powerbi_master[Yield_Qtl_Per_Acre]), powerbi_master[Year] = LastYear)
) * 100

-- Revenue per Acre
Revenue per Acre = AVERAGE(powerbi_master[Revenue_Per_Acre])
```

---

## 5. Publishing to Power BI Service

```
1. File → Publish → Publish to Power BI
2. Select your workspace
3. In Power BI Service → Dataset Settings → Scheduled Refresh
4. Set refresh frequency: Daily at 7:00 AM
5. Share dashboard URL with stakeholders
```

---

## 6. Troubleshooting

| Issue | Fix |
|-------|-----|
| Data not loading | Check file paths in Data Source Settings |
| Blank AI Insights page | Run `python scripts/chatgpt_analyzer.py` first |
| Missing columns | Ensure `run_pipeline.py` completed without errors |
| Theme not applying | Re-import `theme/farm_theme.json` manually |
