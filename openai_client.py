"""openai_client.py — Author: Mousumi Paul"""
import os
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError: pass
try:
    from openai import OpenAI
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    OPENAI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
except Exception: OPENAI_AVAILABLE = False

GPT_MODEL=os.getenv("GPT_MODEL","gpt-4o"); MAX_TOKENS=int(os.getenv("GPT_MAX_TOKENS","600")); TEMPERATURE=float(os.getenv("GPT_TEMPERATURE","0.4"))

MOCK_RESPONSES={
    "yield":"Yields have shown a steady upward trajectory driven by improved seed varieties and irrigation. The top-performing region consistently outperforms the national average by 18-22%. Profit margins remain healthy above 30%. Recommendation: expand drip irrigation to sustain growth.",
    "weather":"Weather patterns significantly influence agricultural output, with monsoon months showing strongest correlation with Kharif yields. Temperature extremes above 40C depress Rabi harvests in northern regions. Deeper-rooted crops show more weather resilience.",
    "seasonal":"Kharif season dominates production volume at roughly 55% of annual output. Rabi season drives quality-premium crops. Zaid commands premium pricing despite smaller volume. Prioritize cold storage capacity ahead of Kharif harvest peaks.",
}

def ask_gpt(prompt, context="yield"):
    if not OPENAI_AVAILABLE:
        print("    [MOCK MODE] No API key — using sample AI response")
        return MOCK_RESPONSES.get(context, MOCK_RESPONSES["yield"])
    try:
        r=_client.chat.completions.create(model=GPT_MODEL,max_tokens=MAX_TOKENS,temperature=TEMPERATURE,messages=[{"role":"system","content":"You are an expert agricultural data analyst. Give concise, actionable insights in plain English. 3-5 sentences. Be specific with numbers."},{"role":"user","content":prompt}])
        return r.choices[0].message.content.strip()
    except Exception as e:
        print(f"    [API ERROR] {e}"); return MOCK_RESPONSES.get(context, MOCK_RESPONSES["yield"])
