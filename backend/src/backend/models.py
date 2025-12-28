from pydantic import BaseModel, Field
from typing import List, Optional

class FlightOption(BaseModel):
    airline: str = Field(..., description="Name of the airline")
    flight_number: str = Field(..., description="Flight number")
    departure_time: str = Field(..., description="Departure time in ISO format")
    arrival_time: str = Field(..., description="Arrival time in ISO format")
    duration: str = Field(..., description="Duration of the flight")
    price: float = Field(..., description="Price in USD")
    stops: int = Field(..., description="Number of stops")

class FlightOutput(BaseModel):
    options: List[FlightOption] = Field(..., description="List of flight options found")
    message: Optional[str] = Field(None, description="Message if no flights found or skipped")

class HotelOption(BaseModel):
    name: str = Field(..., description="Name of the hotel")
    rating: float = Field(..., description="Star rating of the hotel")
    location: str = Field(..., description="Location or address")
    price_per_night: float = Field(..., description="Price per night in USD")
    amenities: List[str] = Field(..., description="List of amenities")

class HotelOutput(BaseModel):
    options: List[HotelOption] = Field(..., description="List of hotel options found")
    message: Optional[str] = Field(None, description="Message if no hotels found or skipped")

class Activity(BaseModel):
    name: str = Field(..., description="Name of the activity")
    description: str = Field(..., description="Description of the activity")
    start_time: str = Field(..., description="Start time")
    end_time: str = Field(..., description="End time")
    cost: float = Field(..., description="Estimated cost")

class ItineraryDay(BaseModel):
    day: int = Field(..., description="Day number")
    activities: List[Activity] = Field(..., description="List of activities for the day")

class ItineraryOutput(BaseModel):
    days: List[ItineraryDay] = Field(..., description="List of daily itineraries")
    total_estimated_cost: float = Field(..., description="Total estimated cost of the itinerary")
