from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


@CrewBase
class FinancialAgent:
    """FinancialAgent crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    search_tool = ScrapeWebsiteTool()
    serper_tool = SerperDevTool()

    @agent
    def crypto_market_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["crypto_market_strategist"],
            verbose=True,
            allow_delegation=True,
            tools=[self.search_tool, self.serper_tool],
            llm=llm,
        )

    @agent
    def sentiment_analysis_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["sentiment_analysis_specialist"],
            verbose=True,
            allow_delegation=True,
            tools=[self.search_tool, self.serper_tool],
            llm=llm,
        )

    @agent
    def risk_management_consultant(self) -> Agent:
        return Agent(
            config=self.agents_config["risk_management_consultant"],
            verbose=True,
            allow_delegation=True,
            tools=[self.search_tool, self.serper_tool],
            llm=llm,
        )

    @agent
    def technical_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_market_analyst"],
            verbose=True,
            allow_delegation=True,
            tools=[self.search_tool, self.serper_tool],
            llm=llm,
        )

    @task
    def market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["market_analysis_task"],
            async_execution=True,
            output_file="reports/Market_Analysis.md",
        )

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["sentiment_analysis_task"],
            async_execution=True,
            output_file="reports/Sentiment_Analysis.md",
        )

    @task
    def risk_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config["risk_assessment_task"],
            async_execution=True,
            output_file="reports/Risk_Assessment.md",
        )

    @task
    def technical_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["technical_analysis_task"],
            async_execution=True,
            output_file="reports/Technical_Analysis.md",
        )

    @task
    def investment_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config["investment_recommendation_task"],
            context=[
                self.market_analysis_task(),
                self.sentiment_analysis_task(),
                self.risk_assessment_task(),
                self.technical_analysis_task(),
            ],
            output_file="reports/Recommendation.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FinancialAgent crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=llm,
            verbose=True,
        )
