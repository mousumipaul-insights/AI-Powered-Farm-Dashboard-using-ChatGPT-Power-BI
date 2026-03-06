"""
insight_parser.py
Author: Mousumi Paul
Parses, validates, and structures ChatGPT responses for downstream use.
"""

import json
import re
from typing import Union


def clean_json_response(raw: str) -> str:
    """Strip markdown code fences and whitespace from API response."""
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


def parse_json_insight(raw: str) -> dict:
    """Parse JSON from ChatGPT response with error handling."""
    try:
        return json.loads(clean_json_response(raw))
    except json.JSONDecodeError as e:
        return {
            "parse_error": str(e),
            "raw_response": raw[:500],
            "status": "failed"
        }


def validate_yield_insight(data: dict) -> dict:
    """Validate yield analysis response has required fields."""
    required = ["top_performing_crops", "trend_direction", "key_findings"]
    missing  = [k for k in required if k not in data]
    data["validation_status"] = "OK" if not missing else f"Missing: {missing}"
    return data


def validate_weather_insight(data: dict) -> dict:
    required = ["rainfall_impact_level", "optimal_rainfall_range_mm", "plain_language_summary"]
    missing  = [k for k in required if k not in data]
    data["validation_status"] = "OK" if not missing else f"Missing: {missing}"
    return data


def flatten_insights_for_powerbi(insights: dict, prefix: str = "") -> dict:
    """
    Flatten nested JSON from ChatGPT into a flat dict for Power BI embedding.
    Lists are joined as semicolon-separated strings.
    """
    flat = {}
    for k, v in insights.items():
        key = f"{prefix}{k}" if prefix else k
        if isinstance(v, list):
            flat[key] = "; ".join(str(i) for i in v)
        elif isinstance(v, dict):
            flat.update(flatten_insights_for_powerbi(v, prefix=f"{key}_"))
        else:
            flat[key] = v
    return flat


def insights_to_dataframe(insights_dict: dict):
    """Convert flattened insights to a pandas DataFrame for Excel export."""
    import pandas as pd
    flat = flatten_insights_for_powerbi(insights_dict)
    return pd.DataFrame([{"Field": k, "AI_Output": v} for k, v in flat.items()])


def extract_key_metrics(yield_insight: dict, weather_insight: dict, seasonal_insight: dict) -> dict:
    """Pull the single most important metric from each analysis for KPI card."""
    return {
        "Yield_Trend":          yield_insight.get("trend_direction", "Unknown"),
        "Top_Crop":             (yield_insight.get("top_performing_crops", ["—"])[0] if
                                 yield_insight.get("top_performing_crops") else "—"),
        "Rainfall_Impact":      weather_insight.get("rainfall_impact_level", "Unknown"),
        "Optimal_Rainfall":     weather_insight.get("optimal_rainfall_range_mm", "—"),
        "Best_Profit_Season":   seasonal_insight.get("highest_profit_season", "—"),
        "Top_Kharif_Crop":      (seasonal_insight.get("best_kharif_crops", ["—"])[0] if
                                 seasonal_insight.get("best_kharif_crops") else "—"),
        "Top_Rabi_Crop":        (seasonal_insight.get("best_rabi_crops", ["—"])[0] if
                                 seasonal_insight.get("best_rabi_crops") else "—"),
    }
