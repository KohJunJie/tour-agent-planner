from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import random


class HotelSearchInput(BaseModel):
    """Input schema for HotelSearchTool."""

    destination: str = Field(..., description="Destination city or area name")
    check_in_date: str = Field(..., description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(..., description="Check-out date in YYYY-MM-DD format")
    budget: Optional[str] = Field(
        None, description="Budget range: 'budget', 'mid-range', 'luxury', or 'any'"
    )


class HotelSearchTool(BaseTool):
    name: str = "Hotel Search Tool"
    description: str = (
        "Searches for available hotels in the destination area. "
        "Returns mock hotel data including name, rating, price, amenities, and location. "
        "Useful for finding accommodation options for travel planning."
    )
    args_schema: Type[BaseModel] = HotelSearchInput

    def _run(
        self,
        destination: str,
        check_in_date: str,
        check_out_date: str,
        budget: Optional[str] = "any",
    ) -> str:
        """Generate mock hotel data for testing."""

        hotel_names = [
            "Grand Plaza Hotel",
            "Seaside Resort & Spa",
            "Downtown Marriott",
            "Hilton Garden Inn",
            "Comfort Inn & Suites",
            "The Luxury Collection",
            "Holiday Inn Express",
            "Best Western Plus",
            "Hyatt Regency",
            "Courtyard by Marriott",
            "Four Seasons Hotel",
            "Radisson Blu",
        ]

        locations = [
            "Downtown",
            "Near Airport",
            "City Center",
            "Waterfront",
            "Historic District",
            "Business District",
            "Near Convention Center",
        ]

        amenities_pool = [
            "Free WiFi",
            "Breakfast included",
            "Fitness center",
            "Swimming pool",
            "Parking available",
            "Restaurant on-site",
            "Bar/Lounge",
            "Room service",
            "Business center",
            "Spa services",
            "Airport shuttle",
            "Pet friendly",
        ]

        # Calculate number of nights
        from datetime import datetime

        try:
            checkin = datetime.strptime(check_in_date, "%Y-%m-%d")
            checkout = datetime.strptime(check_out_date, "%Y-%m-%d")
            num_nights = (checkout - checkin).days
        except:
            num_nights = 3

        # Generate 6 hotel options
        hotels = []

        for i in range(6):
            star_rating = random.randint(3, 5)
            guest_rating = round(random.uniform(3.5, 4.9), 1)
            num_reviews = random.randint(150, 2500)

            # Price based on star rating
            if star_rating == 5:
                price_per_night = random.randint(250, 500)
                category = "Luxury"
            elif star_rating == 4:
                price_per_night = random.randint(120, 250)
                category = "Mid-range"
            else:
                price_per_night = random.randint(60, 120)
                category = "Budget"

            total_price = price_per_night * num_nights

            # Select amenities based on rating
            num_amenities = 4 + star_rating
            selected_amenities = random.sample(amenities_pool, k=num_amenities)

            hotel_info = {
                "Name": random.choice(hotel_names),
                "Category": category,
                "Star Rating": f"{star_rating} stars",
                "Guest Rating": f"{guest_rating}/5.0 ({num_reviews} reviews)",
                "Location": f"{random.choice(locations)}, {destination}",
                "Distance": f"{random.uniform(0.3, 5.0):.1f} miles from city center",
                "Price per Night": f"${price_per_night}",
                "Total Price": f"${total_price} ({num_nights} nights)",
                "Amenities": ", ".join(selected_amenities),
            }
            hotels.append(hotel_info)

        # Sort by price
        hotels.sort(key=lambda x: int(x["Price per Night"].replace("$", "")))

        # Format output
        result = f"\n{'='*80}\n"
        result += f"HOTEL SEARCH RESULTS\n"
        result += f"Destination: {destination}\n"
        result += f"Check-in: {check_in_date}\n"
        result += f"Check-out: {check_out_date}\n"
        result += f"Nights: {num_nights}\n"
        result += f"{'='*80}\n\n"

        for idx, hotel in enumerate(hotels, 1):
            result += f"Option {idx} - {hotel['Price per Night']}/night\n"
            result += f"  {hotel['Name']}\n"
            result += f"  Category: {hotel['Category']} | {hotel['Star Rating']}\n"
            result += f"  Guest Rating: {hotel['Guest Rating']}\n"
            result += f"  Location: {hotel['Location']}\n"
            result += f"  Distance: {hotel['Distance']}\n"
            result += f"  Total Price: {hotel['Total Price']}\n"
            result += f"  Amenities: {hotel['Amenities']}\n"
            result += f"\n"

        result += f"Total hotels found: {len(hotels)}\n"
        result += f"Price range: ${min(int(h['Price per Night'].replace('$', '')) for h in hotels)} - "
        result += f"${max(int(h['Price per Night'].replace('$', '')) for h in hotels)} per night\n"

        return result
