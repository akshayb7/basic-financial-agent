#!/usr/bin/env python
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from financial_agent.crew import FinancialAgent

app = FastAPI()

class RunRequest(BaseModel):
    crypto_coin: str = "ETH"
    investment_strategy: str = "Day Trading"

@app.post("/run")
def run(request: RunRequest):
    """
    Run the crew.
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    inputs = {
        "crypto_coin": request.crypto_coin,
        "investment_strategy": request.investment_strategy,
        "date": f"{todays_date}",
    }
    FinancialAgent().crew().kickoff(inputs=inputs)
    return {"status": "success", "inputs": inputs}
