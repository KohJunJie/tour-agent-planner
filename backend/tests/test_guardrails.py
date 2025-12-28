import pytest
from datetime import date, timedelta
from backend.guardrails import validate_input


class TestGuardrails:
    def test_valid_input(self):
        """Test that valid input passes validation."""
        future_date = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        return_date = (date.today() + timedelta(days=37)).strftime("%Y-%m-%d")

        inputs = {
            "origin": "NYC",
            "destination": "LON",
            "departure_date": future_date,
            "return_date": return_date,
            "needs_flights": True,
            "budget": "mid-range",
        }

        result = validate_input(inputs)
        assert result["origin"] == "NYC"
        assert result["departure_date"] == future_date

    def test_past_date_validation(self):
        """Test that past dates raise an error."""
        past_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        inputs = {"departure_date": past_date}

        with pytest.raises(ValueError, match="Date cannot be in the past"):
            validate_input(inputs)

    def test_return_date_before_departure(self):
        """Test that return date before departure date raises an error."""
        future_date = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        earlier_date = (date.today() + timedelta(days=29)).strftime("%Y-%m-%d")

        inputs = {"departure_date": future_date, "return_date": earlier_date}

        with pytest.raises(
            ValueError, match="Return date must be after departure date"
        ):
            validate_input(inputs)

    def test_invalid_date_format(self):
        """Test that invalid date formats raise an error."""
        inputs = {"departure_date": "2025/01/01"}

        with pytest.raises(ValueError, match="Incorrect date format"):
            validate_input(inputs)
