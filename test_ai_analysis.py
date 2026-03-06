"""
test_ai_analysis.py
Author: Mousumi Paul
Unit tests for insight_parser.py and prompt_templates.py
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ai_analysis.insight_parser import (
    clean_json_response, parse_json_insight,
    flatten_insights_for_powerbi, extract_key_metrics
)
from src.ai_analysis.prompt_templates import FarmPrompts


def test_clean_json_strips_markdown():
    raw = "```json\n{\"key\": \"value\"}\n```"
    cleaned = clean_json_response(raw)
    assert cleaned == '{"key": "value"}'
    print("✅ test_clean_json_strips_markdown passed")


def test_parse_valid_json():
    raw = '{"trend_direction": "Improving", "top_performing_crops": ["Rice", "Wheat"]}'
    result = parse_json_insight(raw)
    assert result["trend_direction"] == "Improving"
    assert isinstance(result["top_performing_crops"], list)
    print("✅ test_parse_valid_json passed")


def test_parse_invalid_json_returns_error():
    result = parse_json_insight("This is not JSON at all!!!")
    assert "parse_error" in result or "raw_response" in result
    print("✅ test_parse_invalid_json_returns_error passed")


def test_flatten_nested_dict():
    nested = {
        "trend": "Improving",
        "crops": ["Rice","Wheat"],
        "advice": {"Kharif": "Plant early", "Rabi": "Use certified seeds"}
    }
    flat = flatten_insights_for_powerbi(nested)
    assert flat["trend"] == "Improving"
    assert "Rice; Wheat" == flat["crops"]
    assert flat["advice_Kharif"] == "Plant early"
    print("✅ test_flatten_nested_dict passed")


def test_extract_key_metrics():
    yield_ins = {
        "trend_direction": "Improving",
        "top_performing_crops": ["Sugarcane (62 Qtl)","Tomato","Potato"]
    }
    weather_ins = {
        "rainfall_impact_level": "High",
        "optimal_rainfall_range_mm": "800–1200 mm"
    }
    seasonal_ins = {
        "highest_profit_season": "Rabi",
        "best_kharif_crops": ["Rice","Maize","Cotton"],
        "best_rabi_crops": ["Wheat","Potato","Tomato"]
    }
    metrics = extract_key_metrics(yield_ins, weather_ins, seasonal_ins)
    assert metrics["Yield_Trend"] == "Improving"
    assert metrics["Best_Profit_Season"] == "Rabi"
    assert metrics["Rainfall_Impact"] == "High"
    print("✅ test_extract_key_metrics passed")


def test_prompt_templates_are_strings():
    p1 = FarmPrompts.yield_trend_analysis("sample data")
    p2 = FarmPrompts.weather_impact_analysis("sample data")
    p3 = FarmPrompts.seasonal_recommendations("sample data")
    p4 = FarmPrompts.crop_comparison_report("sample data")
    for p in [p1, p2, p3, p4]:
        assert isinstance(p, str)
        assert len(p) > 50
    print("✅ test_prompt_templates_are_strings passed")


if __name__ == "__main__":
    test_clean_json_strips_markdown()
    test_parse_valid_json()
    test_parse_invalid_json_returns_error()
    test_flatten_nested_dict()
    test_extract_key_metrics()
    test_prompt_templates_are_strings()
    print("\n✅ All AI analysis tests passed!")
