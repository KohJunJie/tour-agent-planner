from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import random
from datetime import datetime, timedelta


class FlightSearchInput(BaseModel):
    """Input schema for FlightSearchTool."""

    origin: str = Field(
        ..., description="Origin airport code or city name (e.g., 'JFK' or 'New York')"
    )
    destination: str = Field(
        ...,
        description="Destination airport code or city name (e.g., 'LAX' or 'Los Angeles')",
    )
    departure_date: str = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: Optional[str] = Field(
        None, description="Return date in YYYY-MM-DD format (optional for one-way)"
    )


class FlightSearchTool(BaseTool):
    name: str = "Flight Search Tool"
    description: str = (
        "Searches for available flights between origin and destination airports. "
        "Returns mock flight data including airline, price, duration, and layover information. "
        "Useful for finding flight options for travel planning."
    )
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
    ) -> str:
        """Generate mock flight data for testing."""

        airlines = [
            "United Airlines",
            "Delta Air Lines",
            "American Airlines",
            "Southwest Airlines",
            "JetBlue Airways",
            "Alaska Airlines",
        ]

        aircraft = ["Boeing 737", "Airbus A320", "Boeing 787", "Airbus A350"]

        # Generate 5 outbound flight options
        flights = []
        base_price = random.randint(200, 800)

        for i in range(5):
            airline = random.choice(airlines)
            flight_num = f"{airline[:2].upper()}{random.randint(100, 9999)}"

            # Random departure time
            dep_hour = random.randint(6, 20)
            dep_minute = random.choice([0, 15, 30, 45])
            departure_time = f"{dep_hour:02d}:{dep_minute:02d}"

            # Flight duration (3-12 hours depending on distance)
            duration_hours = random.randint(3, 12)
            duration_minutes = random.choice([0, 15, 30, 45])
            duration = f"{duration_hours}h {duration_minutes}m"

            # Calculate arrival time
            arrival_hour = (
                dep_hour + duration_hours + (dep_minute + duration_minutes) // 60
            ) % 24
            arrival_minute = (dep_minute + duration_minutes) % 60
            arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"

            # Stops
            num_stops = random.choices([0, 1, 2], weights=[0.4, 0.5, 0.1])[0]
            stops = "Nonstop" if num_stops == 0 else f"{num_stops} stop(s)"

            # Price variation
            price = base_price + random.randint(-100, 300) + (num_stops * 50)

            # Booking class
            booking_class = random.choice(
                ["Economy", "Economy", "Premium Economy", "Business"]
            )

            flight_info = {
                "Flight": f"{airline} {flight_num}",
                "Aircraft": random.choice(aircraft),
                "Departure": f"{departure_date} {departure_time} from {origin}",
                "Arrival": f"{departure_date} {arrival_time} to {destination}",
                "Duration": duration,
                "Stops": stops,
                "Class": booking_class,
                "Price": f"${price} USD",
                "Amenities": ", ".join(
                    random.sample(
                        [
                            "WiFi",
                            "In-flight entertainment",
                            "Power outlets",
                            "Complimentary snacks",
                            "Extra legroom",
                        ],
                        k=random.randint(2, 4),
                    )
                ),
            }
            flights.append(flight_info)

        # Sort by price
        flights.sort(key=lambda x: int(x["Price"].replace("$", "").replace(" USD", "")))

        # Format output
        result = f"\n{'='*80}\n"
        result += f"FLIGHT SEARCH RESULTS\n"
        result += f"Route: {origin} → {destination}\n"
        result += f"Departure Date: {departure_date}\n"
        if return_date:
            result += f"Return Date: {return_date}\n"
        result += f"{'='*80}\n\n"

        for idx, flight in enumerate(flights, 1):
            result += f"Option {idx} - {flight['Price']}\n"
            result += f"  Flight: {flight['Flight']}\n"
            result += f"  Aircraft: {flight['Aircraft']}\n"
            result += f"  Departure: {flight['Departure']}\n"
            result += f"  Arrival: {flight['Arrival']}\n"
            result += f"  Duration: {flight['Duration']}\n"
            result += f"  Stops: {flight['Stops']}\n"
            result += f"  Class: {flight['Class']}\n"
            result += f"  Amenities: {flight['Amenities']}\n"
            result += f"\n"

        if return_date:
            result += f"\n{'='*80}\n"
            result += f"RETURN FLIGHTS\n"
            result += f"Route: {destination} → {origin}\n"
            result += f"Date: {return_date}\n"
            result += f"{'='*80}\n"
            result += f"(Similar options available for return journey)\n\n"

        result += f"Total options found: {len(flights)}\n"
        result += f"Price range: ${min(int(f['Price'].replace('$', '').replace(' USD', '')) for f in flights)} - ${max(int(f['Price'].replace('$', '').replace(' USD', '')) for f in flights)} USD\n"

        return result
