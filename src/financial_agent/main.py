#!/usr/bin/env python
from fastapi import FastAPI
from datetime import datetime
from financial_agent.crew import FinancialAgent

app = FastAPI()

@app.post("/run")
def run(crypto_coin: str = "ETH", investment_strategy: str = "Day Trading"):
    """
    Run the crew.
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    inputs = {
        "crypto_coin": crypto_coin,
        "investment_strategy": investment_strategy,
        "date": f"{todays_date}",
    }
    FinancialAgent().crew().kickoff(inputs=inputs)
    return {"status": "success", "inputs": inputs}
