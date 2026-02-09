
import sys
import io

# Force stdout to use UTF-8 so emojis don't crash Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import subprocess
import sys
PIPELINE_STEPS = [
    "scripts/load/load.py",
    "scripts/transform/transform.py",       # Fixed folder name
    "scripts/analytics/build_fact_sales.py",
    "scripts/analytics/build_aggregates.py",
    "scripts/quality/data_quality_checks.py"
]

def run_step(step):
    print(f"\n🚀 Running: {step}")
    
    # sys.executable points to E:\...\venv\Scripts\python.exe
    # This prevents the 'ModuleNotFoundError'
    result = subprocess.run(
        [sys.executable, step], 
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print(f"❌ Pipeline failed at {step}")
        print(result.stderr)
        sys.exit(1)

    print(f"✅ Completed: {step}")

if __name__ == "__main__":
    print("\n🔥 STARTING FULL RETAIL ETL PIPELINE 🔥")

    for step in PIPELINE_STEPS:
        run_step(step)

    print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY 🎉")