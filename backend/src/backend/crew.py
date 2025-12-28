from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from backend.tools import FlightSearchTool, HotelSearchTool
from backend.models import FlightOutput, HotelOutput, ItineraryOutput

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class Backend:
    """Backend crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def flight_retriever(self) -> Agent:
        return Agent(
            config=self.agents_config["flight_retriever"],  # type: ignore[index]
            verbose=True,
            tools=[FlightSearchTool()],
        )

    @agent
    def hotel_finder(self) -> Agent:
        google_maps_mcp = MCPServerAdapter(
            serverparams=StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-google-maps"],
                env={"GOOGLE_MAPS_API_KEY": os.environ.get("GOOGLE_MAPS_API_KEY", "")},
            )
        )

        return Agent(
            config=self.agents_config["hotel_finder"],  # type: ignore[index]
            tools=[HotelSearchTool(), google_maps_mcp],
            verbose=True,
        )

    @agent
    def itinerary_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["itinerary_planner"],  # type: ignore[index]
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def retrieve_flights_task(self) -> Task:
        return Task(
            config=self.tasks_config["retrieve_flights_task"],  # type: ignore[index]
            output_pydantic=FlightOutput,
        )

    @task
    def find_hotels_task(self) -> Task:
        return Task(
            config=self.tasks_config["find_hotels_task"],  # type: ignore[index]
            output_pydantic=HotelOutput,
        )

    @task
    def plan_itinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config["plan_itinerary_task"],  # type: ignore[index]
            output_pydantic=ItineraryOutput,
        )

    def travel_manager(self) -> Agent:
        return Agent(config=self.agents_config["manager"], verbose=True)  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        """Creates the Backend crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=self.travel_manager(),
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
