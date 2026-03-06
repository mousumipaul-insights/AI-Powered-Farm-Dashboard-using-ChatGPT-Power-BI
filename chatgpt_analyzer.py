"""
chatgpt_analyzer.py
Author: Mousumi Paul
ChatGPT integration for AI Farm Dashboard — includes mock mode for demo/testing
"""
import os, json, pandas as pd
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError: pass

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")
USE_MOCK = not bool(OPENAI_API_KEY)

if not USE_MOCK:
    try:
        from openai import OpenAI; client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError: USE_MOCK = True

def call_chatgpt(prompt, max_tokens=800):
    if USE_MOCK: return _mock(prompt)
    resp = client.chat.completions.create(
        model="gpt-4o", messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens, temperature=0.3)
    return resp.choices[0].message.content.strip()

def _mock(prompt):
    if "yield" in prompt.lower() or "top_performing" in prompt.lower():
        return json.dumps({"top_performing_crops":["Sugarcane (62.4 Qtl/Acre)","Potato (41.2 Qtl/Acre)","Tomato (36.1 Qtl/Acre)"],"bottom_performing_crops":["Cotton (8.2 Qtl/Acre)","Soybean (12.4 Qtl/Acre)","Groundnut (14.1 Qtl/Acre)"],"year_with_highest_yield":"2024","trend_direction":"Improving","yoy_growth_estimate_pct":7.5,"key_findings":["Average yield improved 7.5% from 2020–2024 driven by better seed varieties and irrigation.","Sugarcane and Potato consistently outperform other crops by yield per acre.","Punjab and West Bengal lead yield performance across most crop types.","Kharif crops benefit most from above-average monsoon rainfall years.","Cotton shows highest price volatility, increasing revenue risk."],"yield_improvement_tips":["Adopt precision drip irrigation for water-intensive crops like Sugarcane.","Use certified high-yield variety (HYV) seeds to improve base productivity.","Time fertilizer application to match crop growth stages for maximum efficiency."]})
    elif "weather" in prompt.lower() or "rainfall" in prompt.lower():
        return json.dumps({"rainfall_impact_level":"High","temperature_impact_level":"Medium","most_weather_sensitive_crop":"Rice","least_weather_sensitive_crop":"Wheat","optimal_rainfall_range_mm":"800–1200 mm","optimal_temp_range_c":"22–28 °C","weather_risk_factors":["Monsoon delays of 2+ weeks reduce Kharif crop yields by up to 18%.","Heat stress above 35°C during wheat flowering cuts output by 12–15%.","Unseasonal October rains damage Rabi crop quality and depress market prices."],"climate_adaptation_tips":["Install soil moisture sensors to trigger precision irrigation during dry spells.","Select drought-tolerant crop varieties for Rajasthan and Gujarat regions.","Adopt crop insurance schemes to manage weather-induced revenue risk."],"plain_language_summary":"Rainfall is the dominant weather driver for yield outcomes, especially for Kharif crops like Rice and Maize. Temperature extremes during critical growth stages pose secondary but significant risk. Farmers in arid zones are most vulnerable to weather-induced yield loss."})
    elif "season" in prompt.lower() or "kharif" in prompt.lower():
        return json.dumps({"best_kharif_crops":["Rice","Maize","Soybean"],"best_rabi_crops":["Wheat","Potato","Tomato"],"best_zaid_crops":["Watermelon","Muskmelon"],"highest_profit_season":"Rabi","seasonal_advice":{"Kharif":"Prioritize Rice in high-rainfall zones and Cotton in semi-arid belts. Sow by first week of June to align with monsoon onset for optimal germination.","Rabi":"Focus on Wheat and Potato for consistent profitability. Plant after October 15 to avoid warm-weather germination failures in north India.","Zaid":"Use short-duration vegetables for quick returns. Ensure dedicated irrigation access before committing Zaid area."},"crop_rotation_suggestion":"Rotate Kharif Rice with Rabi Wheat, then add a legume (Soybean/Groundnut) every 3rd year to restore soil nitrogen.","risk_warnings":["Late Kharif sowing (after June 20) increases pest pressure and reduces yield by 10–12%.","Rabi crops in north India face frost risk in January — prepare protective measures by December.","Zaid crops are highly price-volatile; sell within 5 days of harvest to avoid spoilage losses."]})
    else:
        return "Crop Performance Summary (2020–2024):\n\nBased on 2020–2024 data, Sugarcane delivers the highest yield at 62 Qtl/Acre making it the volume leader, while Tomato offers the best profit margin at 38% on average. Wheat remains the most reliable Rabi crop for small farmers due to stable MSP support and lower input risk. Cotton shows high revenue potential but carries significant weather and market price volatility, making it unsuitable for risk-averse farmers with less than 10 acres. For portfolio diversification, a combination of one high-yield cereal (Rice or Wheat), one cash crop (Cotton or Sugarcane on larger holdings), and one vegetable (Tomato or Potato) is recommended to balance yield stability with profit potential across seasons."

def parse_json(text):
    try:
        clean = text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(clean)
    except: return {"raw_response": text}

def main():
    path = "data/processed/yield_weather_merged.csv"
    if not os.path.exists(path):
        os.system("python scripts/data_processing.py")
    df = pd.read_csv(path)
    mode = "🤖 LIVE (OpenAI API)" if not USE_MOCK else "🎭 MOCK (demo mode — no API key)"
    print(f"\n🌾 ChatGPT Analysis — {mode}\n")

    yield_summary = df.groupby("Crop").agg(Avg_Yield=("Yield_Qtl_Per_Acre","mean"),Avg_Profit=("Net_Profit_INR","mean"),Avg_Margin=("Profit_Margin_Pct","mean")).round(2).to_string()
    weather_summary = df.groupby("Region").agg(Avg_Temp=("Avg_Temp_C","mean"),Avg_Rainfall=("Total_Rainfall_MM","mean"),Avg_Yield=("Yield_Qtl_Per_Acre","mean")).round(2).to_string() if "Avg_Temp_C" in df.columns else "Weather data merged"
    seasonal_summary = df.groupby(["Season","Crop"]).agg(Avg_Yield=("Yield_Qtl_Per_Acre","mean"),Avg_Profit=("Net_Profit_INR","mean")).round(2).to_string()
    crop_summary = yield_summary

    yield_prompt = f"You are an expert agricultural data scientist.\nAnalyze this yield data:\n{yield_summary}\nReturn JSON with: top_performing_crops, bottom_performing_crops, year_with_highest_yield, trend_direction, key_findings, yield_improvement_tips"
    weather_prompt = f"Analyze weather vs yield:\n{weather_summary}\nReturn JSON with: rainfall_impact_level, temperature_impact_level, optimal_rainfall_range_mm, weather_risk_factors, plain_language_summary"
    seasonal_prompt = f"Analyze seasonal farm data:\n{seasonal_summary}\nReturn JSON with: best_kharif_crops, best_rabi_crops, highest_profit_season, seasonal_advice, risk_warnings"
    crop_prompt = f"Write 200-word crop comparison:\n{crop_summary}\nStart: 'Crop Performance Summary (2020–2024):'"

    yield_ins    = parse_json(call_chatgpt(yield_prompt))
    weather_ins  = parse_json(call_chatgpt(weather_prompt))
    seasonal_ins = parse_json(call_chatgpt(seasonal_prompt))
    crop_report  = call_chatgpt(crop_prompt, 400)

    os.makedirs("data/chatgpt_outputs", exist_ok=True)
    with open("data/chatgpt_outputs/yield_insights.json","w") as f: json.dump(yield_ins, f, indent=2)
    with open("data/chatgpt_outputs/weather_impact_summary.json","w") as f: json.dump(weather_ins, f, indent=2)
    with open("data/chatgpt_outputs/seasonal_recommendations.json","w") as f: json.dump(seasonal_ins, f, indent=2)
    with open("data/chatgpt_outputs/crop_comparison_report.txt","w") as f: f.write(crop_report)

    print("✅ yield_insights.json")
    print("✅ weather_impact_summary.json")
    print("✅ seasonal_recommendations.json")
    print("✅ crop_comparison_report.txt")
    print(f"\n📋 Trend: {yield_ins.get('trend_direction','—')} | Best Season: {seasonal_ins.get('highest_profit_season','—')}")

if __name__ == "__main__":
    main()
