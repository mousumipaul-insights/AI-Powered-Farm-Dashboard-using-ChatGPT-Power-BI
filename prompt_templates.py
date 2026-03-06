"""
prompt_templates.py
Author: Mousumi Paul
All ChatGPT prompt templates for agricultural analysis use cases.
"""


class FarmPrompts:
    """
    Centralized prompt library for the AI Farm Dashboard.
    Each method returns a formatted prompt string ready for the OpenAI API.
    """

    @staticmethod
    def yield_trend_analysis(data_summary: str) -> str:
        return f"""You are an expert agricultural data scientist.

Analyze the following crop yield dataset summary (2020–2024):
{data_summary}

Return a JSON object with these exact keys:
{{
  "top_performing_crops":      [list of top 3 crops with avg yield values],
  "bottom_performing_crops":   [list of bottom 3 crops],
  "year_with_highest_yield":   "YYYY",
  "trend_direction":           "Improving | Declining | Stable",
  "yoy_growth_estimate_pct":   number,
  "key_findings":              [4–5 specific data-driven bullet insights],
  "yield_improvement_tips":    [3 actionable, specific farming recommendations]
}}
Respond ONLY with valid JSON. No markdown, no explanation."""

    @staticmethod
    def weather_impact_analysis(weather_summary: str) -> str:
        return f"""You are an agricultural meteorologist specializing in South Asian farming.

Analyze weather-yield correlations from this data:
{weather_summary}

Return a JSON object with:
{{
  "rainfall_impact_level":        "High | Medium | Low",
  "temperature_impact_level":     "High | Medium | Low",
  "most_weather_sensitive_crop":  "crop name",
  "least_weather_sensitive_crop": "crop name",
  "optimal_rainfall_range_mm":    "X–Y mm",
  "optimal_temp_range_c":         "X–Y °C",
  "weather_risk_factors":         [3 specific risks with quantified impact],
  "climate_adaptation_tips":      [3 actionable adaptation strategies],
  "plain_language_summary":       "2–3 sentence summary for farmers"
}}
Respond ONLY with valid JSON. No markdown."""

    @staticmethod
    def seasonal_recommendations(seasonal_summary: str) -> str:
        return f"""You are a precision farming advisor for Indian agriculture.

Based on seasonal performance data:
{seasonal_summary}

Return a JSON object with:
{{
  "best_kharif_crops":      [top 3 crops for June–October season],
  "best_rabi_crops":        [top 3 crops for November–March season],
  "best_zaid_crops":        [top 2 crops for April–June season],
  "highest_profit_season":  "Kharif | Rabi | Zaid",
  "seasonal_advice": {{
    "Kharif": "specific, actionable advice string",
    "Rabi":   "specific, actionable advice string",
    "Zaid":   "specific, actionable advice string"
  }},
  "crop_rotation_suggestion": "1-sentence rotation strategy",
  "risk_warnings":            [2–3 seasonal risk warnings with timing]
}}
Respond ONLY with valid JSON. No markdown."""

    @staticmethod
    def crop_comparison_report(crop_summary: str) -> str:
        return f"""You are a farm business consultant writing for Indian farmers.

Compare these crops based on profitability and yield data:
{crop_summary}

Write a clear, practical 200-word comparison report covering:
1. Most profitable crop and why
2. Highest yielding crop
3. Best value crop for small (< 5 acre) farmers
4. Crop diversification recommendation

Format: Plain text starting with "Crop Performance Summary (2020–2024):"
Be specific with numbers. Write in simple, farmer-friendly language."""

    @staticmethod
    def anomaly_detection(yield_data: str) -> str:
        return f"""You are a data quality analyst for agricultural datasets.

Identify unusual patterns or anomalies in this crop yield data:
{yield_data}

Return a JSON object with:
{{
  "anomalies_found": true/false,
  "anomaly_count": number,
  "anomaly_details": [
    {{
      "crop": "name",
      "year": "YYYY",
      "region": "name",
      "issue": "description",
      "severity": "High | Medium | Low"
    }}
  ],
  "likely_causes": [list of probable explanations],
  "recommended_action": "what to do with anomalous records"
}}
Respond ONLY with valid JSON. No markdown."""

    @staticmethod
    def region_performance_summary(region_data: str) -> str:
        return f"""You are a regional agricultural analyst.

Summarize farm performance across regions:
{region_data}

Return a JSON object with:
{{
  "top_region":          "name",
  "bottom_region":       "name",
  "regional_insights":   [3–4 specific regional observations],
  "best_crop_per_region": {{"RegionName": "best crop", ...}},
  "investment_priorities": [2 specific regions needing improvement focus]
}}
Respond ONLY with valid JSON. No markdown."""
