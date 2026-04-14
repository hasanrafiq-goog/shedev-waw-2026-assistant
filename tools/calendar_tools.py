"""Custom tools for Personal Assistant Agent."""

import datetime
import pytz
import os
from typing import Optional, Any
from google.adk.tools import ToolContext
from google.adk.tools.google_api_tool.google_api_toolsets import CalendarToolset
from config import Config
import requests


# ============================================================================
# Non-authenticated tools
# ============================================================================

def get_current_datetime(tool_context: ToolContext) -> str:
    """
    Get the current date and time in the configured timezone.

    Returns:
        Current date and time with day of week
    """
    try:
        # Get timezone from config
        tz = pytz.timezone(Config.TIMEZONE)
        now = datetime.datetime.now(tz)

        # Format: "Monday, April 13, 2026 at 14:30 (Europe/Warsaw)"
        formatted = now.strftime("%A, %B %d, %Y at %H:%M")

        return f"Current date and time: {formatted} ({Config.TIMEZONE})"

    except Exception as e:
        return f"Error getting current time: {str(e)}"


def search_places(
    tool_context: ToolContext,
    query: str,
    location: Optional[str] = None,
    radius_meters: Optional[int] = None,
    min_rating: Optional[float] = None
) -> str:
    """
    Search for places using Google Places API (New).

    Args:
        query: What to search for (e.g., "sushi restaurants", "cafes", "movie theaters")
        location: Location to search near (e.g., "Warsaw, Poland"). Uses default from config if not provided
        radius_meters: Search radius in meters. Uses default from config if not provided
        min_rating: Minimum rating filter (1.0-5.0). Uses default from config if not provided

    Returns:
        Formatted list of places with details (name, rating, address, etc.)
    """
    try:
        # Check if API key is configured
        if not Config.PLACES_API_KEY:
            return "Error: GOOGLE_PLACES_API_KEY not configured in .env file"

        # Use defaults from config if not provided
        if location is None:
            location = Config.DEFAULT_LOCATION
        if radius_meters is None:
            radius_meters = Config.SEARCH_RADIUS_METERS
        if min_rating is None:
            min_rating = Config.MIN_RATING

        # Use Places API (New) - Text Search
        url = "https://places.googleapis.com/v1/places:searchText"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": Config.PLACES_API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.priceLevel,places.types"
        }

        data = {
            "textQuery": f"{query} near {location}",
            "maxResultCount": Config.MAX_SEARCH_RESULTS,
            "rankPreference": "RELEVANCE"
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        places = result.get('places', [])

        if not places:
            return f"No places found for '{query}' near {location}"

        # Filter by rating if specified
        if min_rating:
            places = [p for p in places if p.get('rating', 0) >= min_rating]

        if not places:
            return f"No places found with rating >= {min_rating} for '{query}' near {location}"

        # Format results
        output = [f"Found {len(places)} places for '{query}' near {location}:\n"]

        for i, place in enumerate(places, 1):
            name = place.get('displayName', {}).get('text', 'Unknown')
            address = place.get('formattedAddress', 'No address')
            rating = place.get('rating', 'No rating')
            rating_count = place.get('userRatingCount', 0)

            output.append(
                f"{i}. {name}\n"
                f"   Rating: {rating} ({rating_count} reviews)\n"
                f"   Address: {address}\n"
            )

        return "\n".join(output)

    except Exception as e:
        return f"Error searching places: {str(e)}\n" \
               f"Note: Make sure Google Places API is enabled and API key is valid"


# ============================================================================
# Authenticated Calendar Tools using ADK's CalendarToolset
# ============================================================================

# Create Calendar toolset with OAuth2 authentication
# ADK's CalendarToolset handles OAuth popup flow automatically
calendar_tool_set = CalendarToolset(
    client_id=Config.CALENDAR_CLIENT_ID,
    client_secret=Config.CALENDAR_CLIENT_SECRET,
)
