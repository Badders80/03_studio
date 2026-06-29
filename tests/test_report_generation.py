import pytest
import sys
import os

# Add the parent directory to sys.path to allow importing from scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.generate_investor_report import calculate_payout

def test_payout_calculation():
    # Stakes: 25150 * 0.05 * 0.75 / 20 = 47.156 NZD
    # AED: 47.16 * 2.05 = 96.67
    data = {"total_eligible_nzd": 25150.00, "tokens": 20, "fx": 2.05}
    payout = calculate_payout(data)
    # Matching the math in the logic implementation (96.67)
    assert payout == 96.67

def test_report_generation_cli():
    import subprocess
    cmd = [
        "python3", "03_studio/scripts/generate_investor_report.py",
        "--total_eligible_nzd", "25150",
        "--tokens", "20",
        "--fx", "2.05",
        "--output", "03_studio/output/test_report.html"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists("03_studio/output/test_report.html")
    # Clean up
    if os.path.exists("03_studio/output/test_report.html"):
        os.remove("03_studio/output/test_report.html")
