"""
Performance tests for agents and tools.
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from backend.crew import Backend
from backend.tools import FlightSearchTool, HotelSearchTool


class TestPerformance:
    """Performance tests for agents and tools."""

    @pytest.fixture
    def crew_instance(self):
        """Create a Backend crew instance for testing."""
        # Mock the crew creation to avoid hierarchical process validation
        with patch.object(Backend, "crew") as mock_crew:
            mock_crew.return_value = MagicMock()
            return Backend()

    @pytest.mark.requires_openai
    def test_agent_initialization_speed(self, crew_instance):
        """
        Ensure agents are initialized quickly.
        Threshold: 1.0 second for all agents.
        """
        start_time = time.time()

        # Initialize all agents
        crew_instance.flight_retriever()
        crew_instance.hotel_finder()
        crew_instance.itinerary_planner()

        duration = time.time() - start_time

        # This should be very fast as it just loads config
        assert (
            duration < 1.0
        ), f"Agent initialization took {duration:.4f}s (threshold: 1.0s)"

    def test_flight_tool_performance(self):
        """
        Ensure flight search tool executes quickly.
        Threshold: 0.1 seconds (since it's mocked data).
        """
        tool = FlightSearchTool()

        start_time = time.time()

        # Run the tool with sample data
        tool._run(origin="JFK", destination="LAX", departure_date="2025-01-01")

        duration = time.time() - start_time

        assert duration < 0.1, f"Flight tool took {duration:.4f}s (threshold: 0.1s)"

    def test_hotel_tool_performance(self):
        """
        Ensure hotel search tool executes quickly.
        Threshold: 0.1 seconds (since it's mocked data).
        """
        tool = HotelSearchTool()

        start_time = time.time()

        # Run the tool with sample data
        tool._run(
            destination="Paris", check_in_date="2025-05-01", check_out_date="2025-05-05"
        )

        duration = time.time() - start_time

        assert duration < 0.1, f"Hotel tool took {duration:.4f}s (threshold: 0.1s)"
