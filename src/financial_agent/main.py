from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime
from pydantic import BaseModel
from financial_agent.crew import FinancialAgent

app = FastAPI()
templates = Jinja2Templates(directory="src/financial_agent/templates")


@app.get("/set-env", response_class=HTMLResponse)
def set_env_page(request: Request):
    """
    Render the environment variable setup page.
    """
    return templates.TemplateResponse("set_env.html", {"request": request})


@app.post("/set-env")
def set_env(
    azure_openai_deployment: str = Form(...),
    azure_openai_key: str = Form(...),
    azure_openai_version: str = Form(...),
    azure_openai_endpoint: str = Form(...),
):
    """
    Save environment variables and redirect to the next page.
    """
    os.environ["AZURE_OPENAI_DEPLOYMENT"] = azure_openai_deployment
    os.environ["AZURE_OPENAI_KEY"] = azure_openai_key
    os.environ["AZURE_OPENAI_VERSION"] = azure_openai_version
    os.environ["AZURE_OPENAI_ENDPOINT"] = azure_openai_endpoint

    return RedirectResponse(url="/run-agent", status_code=303)


@app.get("/run-agent", response_class=HTMLResponse)
def run_agent_page(request: Request):
    """
    Render the financial agent run page.
    """
    crypto_coins = ["ETH", "BTC", "SOL", "ADA"]
    investment_strategies = ["Day Trading", "Swing Trading", "HODL", "Scalping"]
    return templates.TemplateResponse(
        "run_agent.html",
        {
            "request": request,
            "crypto_coins": crypto_coins,
            "investment_strategies": investment_strategies,
        },
    )


@app.post("/run")
def run(request: BaseModel):
    """
    Run the financial agent with the provided inputs.
    """
    todays_date = datetime.now().strftime("%Y-%m-%d")
    inputs = {
        "crypto_coin": request.crypto_coin,
        "investment_strategy": request.investment_strategy,
        "date": todays_date,
    }
    FinancialAgent().crew().kickoff(inputs=inputs)
    return {"status": "success", "inputs": inputs}
