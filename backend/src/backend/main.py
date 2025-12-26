#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from backend.crew import Backend

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    # Flexible inputs - leave empty for random destination generation
    inputs = {
        # Travel basics (optional - will generate random if not provided)
        "origin": "",  # e.g., 'JFK' or 'New York'
        "destination": "",  # e.g., 'LAX' or 'Los Angeles'
        # Dates (optional - will use default dates if not provided)
        "departure_date": "",  # YYYY-MM-DD
        "return_date": "",  # YYYY-MM-DD
        "check_in_date": "",  # YYYY-MM-DD
        "check_out_date": "",  # YYYY-MM-DD
        # What to search for (set to False to skip)
        "needs_flights": True,
        "needs_hotels": True,
        "needs_itinerary": True,
        # User preferences (optional)
        "budget": "any",  # 'budget', 'mid-range', 'luxury', or 'any'
        "interests": "",  # e.g., 'beaches, food, culture'
    }

    try:
        Backend().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        Backend().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Backend().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}

    try:
        Backend().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": "",
    }

    try:
        result = Backend().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
