"""
run_pipeline.py
Author: Mousumi Paul
One-click runner for the full AI Farm Dashboard pipeline.
"""

import subprocess
import sys
import time

STEPS = [
    ("🌱 Step 1: Generating sample data",     "scripts/generate_sample_data.py"),
    ("🔧 Step 2: Processing & transforming",  "scripts/data_processing.py"),
    ("🤖 Step 3: Running ChatGPT analysis",   "scripts/chatgpt_analyzer.py"),
    ("📊 Step 4: Building Excel report",      "scripts/export_to_excel.py"),
]

def run_step(label, script):
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    start = time.time()
    result = subprocess.run([sys.executable, script], capture_output=False)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"\n❌ Failed: {script}")
        sys.exit(1)
    print(f"  ⏱  Completed in {elapsed:.1f}s")

def main():
    print("\n" + "🌾 "*18)
    print("  AI-POWERED FARM DASHBOARD — FULL PIPELINE")
    print("  Author: Mousumi Paul")
    print("🌾 "*18)

    for label, script in STEPS:
        run_step(label, script)

    print("\n" + "="*55)
    print("  ✅ PIPELINE COMPLETE!")
    print("="*55)
    print("\n📁 Key outputs:")
    print("  • data/raw/                        ← 4 CSV datasets")
    print("  • data/processed/                  ← Cleaned & merged data")
    print("  • data/chatgpt_outputs/            ← AI analysis JSON files")
    print("  • reports/farm_dashboard_report.xlsx ← Full Excel report")
    print("\n📊 Next step: Open dashboard/powerbi/farm_dashboard.pbix in Power BI Desktop")
    print("   → Update data source to: data/processed/powerbi_master_dataset.xlsx")
    print("   → Click Refresh\n")

if __name__ == "__main__":
    main()
