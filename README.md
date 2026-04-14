# Personal Assistant Agent - SheDev Workshop

A Google ADK-based AI personal assistant that helps you search for places and manage your Google Calendar.

## Features

✨ **Search Places**: Find restaurants, cafes, movie theaters, and more using Google Places API
📅 **Calendar Integration**: Check availability and create calendar events
🤖 **Conversational AI**: Powered by Gemini 2.5 Flash
⚙️ **Configurable**: Easy-to-customize settings for your preferences

## Setup Instructions

### 1. Prerequisites

- A Google Cloud Platform (GCP) project
- Google Cloud Shell (recommended) or local machine with Python 3.9+

### 2. Open Google Cloud Shell

**Recommended for workshop participants:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project
3. Click the **Cloud Shell** icon in the top-right corner (>_)
4. Wait for Cloud Shell to start - it comes with Python, gcloud, and all tools pre-installed!

**Alternative:** If using a local machine, ensure you have:
- Python 3.9 or higher installed
- gcloud CLI installed and configured

### 3. Clone the Repository

In Cloud Shell (or your terminal), clone this repository:

```bash
git clone https://github.com/rafiqhasan/shedev-personal-assistant.git
cd shedev-personal-assistant
```

### 4. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Google Cloud

#### Set Your Project ID

```bash
# Replace YOUR_PROJECT_ID with your actual GCP project ID
export PROJECT_ID="YOUR_PROJECT_ID"
gcloud config set project $PROJECT_ID
```

#### Enable Required APIs

Run these commands to enable all required APIs:

```bash
# Enable Vertex AI API (for Gemini)
gcloud services enable aiplatform.googleapis.com

# Enable Google Calendar API
gcloud services enable calendar-json.googleapis.com

# Enable Places API (New)
gcloud services enable places.googleapis.com
```

**Note:** API enablement may take 1-2 minutes. You'll see confirmation messages when complete.

#### Authenticate with Google Cloud

```bash
gcloud auth application-default login
```

This will open a browser for you to authenticate with your Google account.

### 7. Configure OAuth Consent Screen

Before creating OAuth credentials, you need to configure the OAuth consent screen (first-time setup only):

1. Go to [Google Cloud Console > APIs & Services > OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
2. Choose **User Type**:
   - **Internal**: If using a Google Workspace account (only users in your org can use the app)
   - **External**: If using a personal Gmail account (recommended for workshop)
3. Click **Create**
4. Fill in the required fields:
   - **App name**: `Personal Assistant` (or any name you prefer)
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Click **Save and Continue**
6. **Scopes**: Click **Save and Continue** (we'll add scopes automatically via code)
7. **Test users** (if External):
   - Click **Add Users**
   - Add your email address
   - Click **Save and Continue**
8. Click **Back to Dashboard**

**Note:** For workshop/testing purposes, keeping the app in "Testing" mode is fine. You don't need to publish it.

### 8. Create API Credentials

#### A. Create Places API Key

1. Go to [Google Cloud Console > APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "API Key"
3. Copy the API key
4. (Recommended) Click "Restrict Key":
   - Under "API restrictions", select "Restrict key"
   - Choose "Places API (New)"
   - Click "Save"

#### B. Create Calendar OAuth 2.0 Credentials

1. In the same [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "OAuth client ID"
3. Choose **"Web application"** as application type
4. Name it "Personal Assistant"
5. Under **"Authorized redirect URIs"**, add:
   - `http://localhost:8000/dev-ui/` (for local development)
   - **If using Cloud Shell:** Also add your Cloud Shell redirect URI
   - **CRITICAL:** Include the trailing slash `/` - OAuth will fail without it!
6. Click "Create"
7. **Copy the Client ID and Client Secret** - you'll add these to `.env`

**Note:**
- ADK uses the Google API Toolset which handles OAuth flow with a popup in the web UI
- No JSON credential files needed - just Client ID and Secret in `.env`

### 9. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your details:
```bash
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
ADK_MODEL="gemini-2.5-flash"

# Add your OAuth credentials from step 5B
GOOGLE_CALENDAR_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_CALENDAR_CLIENT_SECRET="your-client-secret"

# Add your Places API key from step 5A
GOOGLE_PLACES_API_KEY="your-places-api-key-here"
```

### 10. Run the Agent

Start the ADK Web UI:

**If using Cloud Shell:**
```bash
# Allow Cloud Shell preview domain for CORS
adk web --allow_origins="regex:https://.*\.cloudshell\.dev"
```

Then:
1. Click **Web Preview** button (top-right of Cloud Shell)
2. Select **Preview on port 8000**
3. A new tab will open with the ADK UI
4. Select `assistant_agent` from the list
5. Start chatting!

**For Cloud Shell users - Finalizing OAuth Redirect URI:**

Since Cloud Shell uses a dynamic URL, you need to add it to your GCP credentials *after* starting the agent:

1. In the ADK UI, try to use a calendar feature (e.g., "What's on my calendar?")
2. You will get an OAuth error page. **Copy the `redirect_uri`** from the error message (it looks like: `https://8000-cs-xxxxx.cloudshell.dev/dev-ui/`)
3. Go back to [Google Cloud Console > Credentials](https://console.cloud.google.com/apis/credentials)
4. Click on your **OAuth 2.0 Client ID**
5. Under **"Authorized redirect URIs"**, click "ADD URI" and paste the exact URL you copied.
6. **IMPORTANT:** Ensure it includes the trailing `/`!
7. Click **Save** and wait 1-2 minutes.
8. Refresh the ADK page and try again - OAuth should now work!

**If using local machine:**
```bash
adk web
```

Then:
1. Open your browser to `http://localhost:8000`
2. Select `assistant_agent` from the list
3. Start chatting!

**Note:** On first use of calendar features:
- ADK's Google API Toolset will trigger an **OAuth authorization popup** in the web UI
- Click "Authorize" and sign in with your Google account
- Grant Calendar permissions (read and write access)
- The popup will close automatically and redirect back to the ADK UI
- Calendar features are now ready to use!
- Credentials are securely stored by ADK for future sessions
- The agent has access to all Google Calendar API operations through the toolset

## Customization

### Edit `config.py` to customize:

- **DEFAULT_LOCATION**: Change from "Warsaw, Poland" to your city
- **SEARCH_RADIUS_METERS**: Adjust search area (default: 5000m / 5km)
- **MIN_RATING**: Minimum rating for place results (default: 4.0)
- **MAX_SEARCH_RESULTS**: Number of results to show (default: 5)
- **TIMEZONE**: Your timezone (default: "Europe/Warsaw")
- **INCLUDE_TRAVEL_TIME**: Add buffer time before events
- **TRAVEL_BUFFER_MINUTES**: Buffer duration if enabled

## Example Interactions

### Check Availability
```
You: Do I have any free time on Friday afternoon?

Agent: [Checks calendar and shows free slots]
```

### Search for Places
```
You: Find me highly rated sushi restaurants in Warsaw

Agent: [Uses Google Maps to find restaurants and displays options]
```

### Full Workflow - Search + Book
```
You: Find a good Italian restaurant for Friday at 7pm and add it to my calendar

Agent:
1. Checks if Friday 7pm is available
2. Searches for Italian restaurants
3. Shows you the options
4. Waits for you to choose
5. Asks for event duration
6. Creates calendar event with your confirmation
```

### Get Free Slots for a Day
```
You: What times am I free on Monday?

Agent: [Shows all available time slots for Monday]
```

## Project Structure

```
shedev-personal-assistant/
├── config.py                    # Configurable settings
├── tools/
│   ├── __init__.py
│   └── calendar_tools.py        # Google Calendar API integration
├── assistant_agent/
│   ├── __init__.py
│   └── agent.py                 # Main agent definition
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .env                         # Your actual config (create this)
├── credentials.json             # OAuth credentials (download from GCP)
├── token.json                   # Auto-generated after first OAuth
└── README.md                    # This file
```

## How It Works

### Tools Available to the Agent:

1. **get_current_datetime** (Custom tool)
   - Returns current date, time, and day of week in configured timezone
   - Used to understand relative dates like "tomorrow" or "next Friday"

2. **search_places** (Custom tool using Google Places API)
   - Searches for places using Google Places API (New)
   - Returns location details, ratings, addresses
   - Configurable search radius and rating filters

3. **calendar_tool_set** (Google API Toolset with OAuth2)
   - Full access to Google Calendar API v3 operations
   - Includes methods for:
     - Listing events (checking availability)
     - Creating events
     - Updating events
     - Deleting events
     - Managing calendar settings
   - OAuth2 authentication with popup flow in ADK web UI
   - Automatically handles token refresh and credential storage

### Agent Workflow:

1. User asks for something (e.g., "Find a restaurant for Friday")
2. Agent decides which tools to use
3. Agent asks for missing information (location, duration, etc.)
4. Agent uses tools to fetch data
5. Agent presents results to user
6. Agent waits for confirmation before making changes
7. Agent executes actions (like creating calendar events)

## Troubleshooting

### "403 Forbidden" errors in Cloud Shell
If you see `403 Forbidden` errors when sending messages in Cloud Shell:
- Stop the server (Ctrl+C)
- Restart with CORS enabled: `adk web --allow_origins="regex:https://.*\.cloudshell\.dev"`
- Refresh the Web Preview browser tab

This error happens because Cloud Shell's Web Preview domain needs to be explicitly allowed for Cross-Origin requests.

### "Calendar API not enabled" or "Places API not enabled"
- Go to GCP Console > APIs & Services > Library
- Search for "Google Calendar API" and "Places API (New)"
- Click "Enable" for both

### "OAuth consent screen not configured"
If you see an error about OAuth consent screen when creating credentials:
- Go to [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent)
- Follow the setup steps in Section 7 above
- Choose "External" for personal Gmail accounts or "Internal" for Workspace accounts
- Add yourself as a test user
- Then retry creating the OAuth credentials

### "Error 400: redirect_uri_mismatch"
This is the most common OAuth error!

**For local machine:**
- Go to Google Cloud Console > Credentials > Your OAuth Client
- Under "Authorized redirect URIs", verify you have:
  - `http://localhost:8000/dev-ui/` (with trailing slash!)
- If missing, click "ADD URI" and add it exactly as shown
- Click "Save" and wait 1-2 minutes for changes to propagate

**For Cloud Shell:**
- The error message shows your redirect URI (e.g., `https://8000-cs-xxxxx.cloudshell.dev/dev-ui/`)
- Copy that **exact URL** from the error message
- Go to Google Cloud Console > Credentials > Your OAuth Client
- Click "ADD URI" and paste the Cloud Shell URL
- **IMPORTANT:** Include the trailing `/` at the end!
- Click "Save" and wait 1-2 minutes
- Refresh your ADK browser tab

**Common mistakes:**
- Missing the trailing `/` will cause this error!
- For Cloud Shell, you must add the specific dynamic URL (it changes each session)

### "Authentication failed" or OAuth popup doesn't appear
- Make sure you added `GOOGLE_CALENDAR_CLIENT_ID` and `GOOGLE_CALENDAR_CLIENT_SECRET` to `.env`
- Verify the OAuth credentials are for a **"Web application"** type (not Desktop app)
- Check that Google Calendar API is enabled in your GCP project
- Ensure redirect URI `http://localhost:8000/dev-ui/` is configured (see above)
- Restart the ADK web server after changing `.env` file

### "Error: GOOGLE_PLACES_API_KEY not configured"
- Make sure you added the API key to your `.env` file
- The API key should be from Google Cloud Console > Credentials

### "Module not found" errors
- Activate virtual environment (if using one)
- Run `pip install -r requirements.txt` again

### Agent doesn't ask for duration
- Check that `ACTIVITY_DURATIONS` is removed from config.py
- The agent is instructed to always ask for duration

### Running on Cloud Shell or Remote Server

**Google Cloud Shell (Recommended):**
- Cloud Shell is the easiest way to run this workshop!
- Web Preview handles port forwarding automatically
- OAuth popup works seamlessly
- No local setup required

**SSH Port Forwarding (for remote servers):**
```bash
# Forward port 8000 to your local machine:
ssh -L 8000:localhost:8000 user@remote-server

# Then access http://localhost:8000 on your local browser
# OAuth popup will work seamlessly!
```

## Workshop Challenges

Try these modifications to learn more:

1. **Change the search location**: Edit `DEFAULT_LOCATION` in `config.py`

2. **Adjust search radius**: Modify `SEARCH_RADIUS_METERS` (in meters)

3. **Enable travel time buffer**: Set `INCLUDE_TRAVEL_TIME = True`

4. **Add a new custom tool**: Create a function in `calendar_tools.py` and add it to the agent

5. **Modify the agent instructions**: Edit `instruction` in `assistant_agent/agent.py` to change behavior

## Resources

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-builder)
- [Google Calendar API Python Quickstart](https://developers.google.com/calendar/api/quickstart/python)
- [Gemini API Documentation](https://ai.google.dev/docs)

## License

This project is created for educational purposes as part of the SheDev workshop.

---

**Happy Coding! 🚀**
