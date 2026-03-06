# 🤖 ChatGPT Prompt Engineering Guide
**Author:** Mousumi Paul

---

## Overview

This project uses 5 distinct prompt strategies to extract agricultural intelligence from ChatGPT. Each is designed with a specific output format, role framing, and temperature setting.

---

## Prompt 1: Yield Trend Analysis

**Goal:** Identify top/bottom crops, growth trend, and actionable tips.

**Role frame:** "You are an expert agricultural data scientist."

**Temperature:** 0.3 (factual, consistent)

**Input:** Grouped summary table (Crop → Avg Yield, Avg Profit, Records)

**Output format:** JSON

```python
prompt = f"""Analyze the following crop yield dataset summary:
{data_summary}

Return JSON with: top_performing_crops, bottom_performing_crops,
year_with_highest_yield, trend_direction, key_findings, yield_improvement_tips"""
```

**Why this works:** Low temperature + explicit JSON schema → reliable, parseable output.

---

## Prompt 2: Weather Impact Analysis

**Goal:** Explain how rainfall and temperature drive yield differences.

**Role frame:** "You are an agricultural meteorologist specializing in South Asian farming."

**Temperature:** 0.3

**Input:** Region-level weather + yield averages

**Output format:** JSON with `plain_language_summary` for non-technical users

**Key design choice:** Asking for both technical metrics AND a plain language summary gives you both a dashboard data field and a human-readable card.

---

## Prompt 3: Seasonal Recommendations

**Goal:** Advise on best crops per season and risk warnings.

**Role frame:** "You are a precision farming advisor for Indian agriculture."

**Temperature:** 0.4 (slightly creative for advice)

**Input:** Season × Crop performance averages

**Output format:** JSON with nested `seasonal_advice` dict

**Key design choice:** The nested JSON structure maps directly to Power BI text card data fields by season.

---

## Prompt 4: Crop Comparison Report

**Goal:** Generate a readable natural language report comparing all crops.

**Role frame:** "You are a farm business consultant writing for Indian farmers."

**Temperature:** 0.6 (more natural language, less rigid)

**Input:** Crop-level summary (yield, profit, margin)

**Output format:** Plain text starting with "Crop Performance Summary:"

**Key design choice:** Plain text (not JSON) is embedded directly in the Power BI AI Insights text card without parsing.

---

## Prompt 5: Anomaly Detection

**Goal:** Flag outlier yield records that may indicate data errors or unusual events.

**Role frame:** "You are a data quality analyst for agricultural datasets."

**Temperature:** 0.2 (very consistent for QA tasks)

**Input:** Records with extreme values

**Output format:** JSON array of anomaly objects

---

## Best Practices Used

### 1. Role Framing
Always start with a domain-specific role: `"You are an expert agricultural data scientist."` This primes the model to use domain vocabulary and reason appropriately.

### 2. Output Specification
Always explicitly specify the output format and list every key. Providing the exact JSON schema dramatically reduces hallucination and parsing failures.

### 3. "Respond ONLY with valid JSON"
Adding this instruction prevents the model from wrapping responses in markdown code blocks or adding preamble text, which breaks JSON parsing.

### 4. Temperature Selection
- **0.2–0.3:** Facts, data analysis, anomaly detection
- **0.4–0.5:** Balanced advice and recommendations
- **0.6–0.7:** Natural language reports and summaries

### 5. Data Summarization Before Sending
Never send raw row-level data to ChatGPT. Always aggregate first (groupby → mean/sum) to:
- Reduce token cost
- Improve response quality
- Stay within context limits

### 6. Mock Mode for Development
The `chatgpt_analyzer.py` includes a `USE_MOCK` flag that returns realistic hardcoded responses when no API key is set. This allows full pipeline testing without spending API credits.

---

## Token Cost Estimates (GPT-4o)

| Prompt Type | Approx Input Tokens | Approx Output Tokens | Est. Cost |
|-------------|:---:|:---:|:---:|
| Yield Trend Analysis | ~400 | ~300 | ~$0.004 |
| Weather Impact | ~350 | ~250 | ~$0.003 |
| Seasonal Recommendations | ~300 | ~300 | ~$0.003 |
| Crop Comparison (text) | ~300 | ~250 | ~$0.003 |
| Anomaly Detection | ~500 | ~200 | ~$0.004 |
| **Total per full run** | | | **~$0.017** |

---

## Extending the Prompts

To add a new analysis type:
1. Add a new `@staticmethod` method to `src/ai_analysis/prompt_templates.py`
2. Add the analysis function to `scripts/chatgpt_analyzer.py`
3. Save output to `data/chatgpt_outputs/`
4. Add the output to the AI Insights sheet in `export_to_excel.py`
5. Create a new Power BI text card pointing to the new field
