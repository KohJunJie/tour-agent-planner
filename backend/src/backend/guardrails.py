from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime, date
from typing import Optional


class TravelInput(BaseModel):
    origin: Optional[str] = Field(None, description="Origin city or airport code")
    destination: Optional[str] = Field(
        None, description="Destination city or airport code"
    )
    departure_date: Optional[str] = Field(
        None, description="Departure date in YYYY-MM-DD format"
    )
    return_date: Optional[str] = Field(
        None, description="Return date in YYYY-MM-DD format"
    )
    check_in_date: Optional[str] = Field(
        None, description="Check-in date in YYYY-MM-DD format"
    )
    check_out_date: Optional[str] = Field(
        None, description="Check-out date in YYYY-MM-DD format"
    )
    needs_flights: bool = True
    needs_hotels: bool = True
    needs_itinerary: bool = True
    budget: str = Field("any", description="Budget preference")
    interests: Optional[str] = Field(None, description="User interests")

    @field_validator("departure_date", "return_date", "check_in_date", "check_out_date")
    @classmethod
    def validate_dates(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        try:
            d = datetime.strptime(v, "%Y-%m-%d").date()
            if d < date.today():
                raise ValueError("Date cannot be in the past")
            return v
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    @field_validator("return_date")
    @classmethod
    def validate_return_date(
        cls, v: Optional[str], info: ValidationInfo
    ) -> Optional[str]:
        if not v or not info.data.get("departure_date"):
            return v

        dep_date = datetime.strptime(info.data["departure_date"], "%Y-%m-%d").date()
        ret_date = datetime.strptime(v, "%Y-%m-%d").date()

        if ret_date < dep_date:
            raise ValueError("Return date must be after departure date")
        return v


def validate_input(inputs: dict) -> dict:
    """
    Validates the input dictionary using the TravelInput Pydantic model.
    Returns the validated dictionary or raises a ValueError.
    """
    try:
        model = TravelInput(**inputs)
        return model.model_dump()
    except Exception as e:
        raise ValueError(f"Input validation failed: {e}")
