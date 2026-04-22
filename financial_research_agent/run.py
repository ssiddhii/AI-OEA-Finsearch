#!/usr/bin/env python3
"""
CLI runner — test the pipeline without Streamlit.
Usage: python run.py AAPL
"""
import sys
from dotenv import load_dotenv

load_dotenv()

if len(sys.argv) < 2:
    print("Usage: python run.py <TICKER>")
    print("Example: python run.py AAPL")
    sys.exit(1)

ticker = sys.argv[1].upper()

from graph.pipeline import run_research

result = run_research(ticker)

print("\n" + "="*60)
print("FINAL REPORT")
print("="*60)
print(result.get("final_report", "No report generated."))

if result.get("errors"):
    print("\n⚠️  Errors encountered:")
    for e in result["errors"]:
        print(f"  - {e}")
