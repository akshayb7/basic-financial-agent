#!/usr/bin/env python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/financial_agent/templates")
from datetime import datetime
from pydantic import BaseModel
from financial_agent.crew import FinancialAgent

app = FastAPI()

class RunRequest(BaseModel):
    crypto_coin: str = "ETH"
    investment_strategy: str = "Day Trading"

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
