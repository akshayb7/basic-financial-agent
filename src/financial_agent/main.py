#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from financial_agent.crew import FinancialAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    inputs = {
        "crypto_coin": "ETH",
        "investment_strategy": "Day Trading",
        "date": f"{todays_date}",
    }
    FinancialAgent().crew().kickoff(inputs=inputs)
