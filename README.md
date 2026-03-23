# AI-Powered Farm Dashboard — ChatGPT + Power BI
**Author:** Mousumi Paul

## Overview
Uses **OpenAI GPT-4o** to analyze agricultural datasets and **Power BI** to visualize:
- Yield Trends (2020–2024)
- Weather Impact (rainfall, temperature correlations)
- Seasonal Patterns (Kharif/Rabi/Zaid)
- AI-Generated Summaries per crop

## Quick Start
```bash
git clone https://github.com/mousumi-paul/ai-farm-dashboard.git
cd ai-farm-dashboard
pip install -r requirements.txt
cp .env.example .env   # Add your OPENAI_API_KEY
python scripts/generate_sample_data.py
python scripts/data_preprocessing.py
python scripts/export_to_excel.py
# Open powerbi/farm_dashboard.pbix and connect to data/processed/dashboard_master.xlsx
```

## Directory Structure
```
ai-farm-dashboard/
├── data/
│   ├── raw/                     # Source CSVs (yield, weather, prices, farmers)
│   ├── processed/               # Power BI data source (dashboard_master.xlsx)
│   └── ai_outputs/              # GPT-generated JSON summaries
├── scripts/
│   ├── generate_sample_data.py
│   ├── data_preprocessing.py
│   ├── chatgpt_analyzer.py      # Calls OpenAI API
│   └── export_to_excel.py       # Builds Power BI Excel workbook
├── src/
│   ├── ai_analysis/             # GPT prompts, client, formatter
│   ├── preprocessing/           # Weather correlator, data cleaner
│   └── visualization/           # KPI calculator
├── notebooks/                   # Jupyter EDA notebooks
├── powerbi/                     # .pbix file + DAX guide
├── docs/                        # Data dictionary, prompt guide
├── config/                      # YAML config for OpenAI
├── tests/                       # Unit tests
├── .env.example
├── requirements.txt
└── .gitignore
```

## Tech Stack
| Layer | Tool |
|-------|------|
| AI Analysis | OpenAI GPT-4o |
| Data Processing | Python, pandas |
| Excel Output | openpyxl |
| BI Dashboard | Power BI |

