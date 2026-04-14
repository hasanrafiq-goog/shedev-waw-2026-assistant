"""Configuration for Personal Assistant Agent."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configurable parameters for the assistant agent."""

    # Google Cloud settings
    GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
    GCP_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    MODEL = os.getenv("ADK_MODEL", "gemini-2.5-flash")

    # Google Calendar OAuth settings
    CALENDAR_CLIENT_ID = os.getenv("GOOGLE_CALENDAR_CLIENT_ID")
    CALENDAR_CLIENT_SECRET = os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET")
    CALENDAR_ID = "primary"
    TIMEZONE = "Europe/Warsaw"

    # Google Places API
    PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

    # Search settings
    DEFAULT_LOCATION = "Warsaw, Poland"
    SEARCH_RADIUS_METERS = 5000  # 5 km
    MIN_RATING = 4.0
    MAX_SEARCH_RESULTS = 5

    # Behavior settings
    AUTO_CREATE_EVENTS = False  # Always ask for confirmation first
    INCLUDE_TRAVEL_TIME = False  # Add buffer time before events
    TRAVEL_BUFFER_MINUTES = 15
