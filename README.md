# Personal Assistant Agent - SheDev Workshop

https://goo.gle/shedev-pl-waw-2026

A Google ADK-based AI personal assistant that helps you search for places and manage your Google Calendar.

## Features

✨ **Search Places**: Find restaurants, cafes, movie theaters, and more using Google Places API
📅 **Calendar Integration**: Check availability and create calendar events
🤖 **Conversational AI**: Powered by Gemini 2.5 Flash
⚙️ **Configurable**: Easy-to-customize settings for your preferences

---

## 🚀 Quick Start (Google Cloud Shell)

This workshop is designed to run entirely in **Google Cloud Shell**. It comes with Python, gcloud, and all necessary tools pre-installed.

### 1. Open Google Cloud Shell

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project.
3. Click the **Cloud Shell** icon in the top-right corner (`>_`).
4. Once Cloud Shell starts, click **"Open Editor"** to get a full IDE experience.

### 2. Clone and Setup

Run these commands in the Cloud Shell terminal:

```bash
# Clone the repository
git clone https://github.com/hasanrafiq-goog/shedev-waw-2026-assistant.git
cd shedev-waw-2026-assistant

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Google Cloud

#### Set Your Project ID
```bash
# Replace YOUR_PROJECT_ID with your actual GCP project ID
export PROJECT_ID="YOUR_PROJECT_ID"
gcloud config set project $PROJECT_ID
```

#### Enable Required APIs
```bash
gcloud services enable aiplatform.googleapis.com \
                       calendar-json.googleapis.com \
                       places.googleapis.com
```

#### Authenticate
```bash
gcloud auth application-default login
```
*Follow the link in the terminal to authorize your account.*

### 4. Configure OAuth Consent Screen

1. Go to [APIs & Services > OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent).
2. You will be guided through the **Google Auth Platform** setup:
   - **1. App Information:** Enter the App name (e.g., `Personal Assistant`) and select your User support email. Click Next.
   - **2. Audience:** Choose **External**. Click Next.
   - **3. Contact Information:** Enter your email address as the Developer contact. Click Next.
   - **4. Finish:** Review and complete the setup.
3. **CRITICAL:** After the initial setup, navigate to the **Audiences** (or **Test users**) section in the Auth Platform menu, click **Add Users**, and add your own email address. If you skip this, the login will fail!

### 5. Create Credentials

#### A. Places API Key
1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials).
2. Click **Create Credentials > API Key**.
3. **Restricting the Key (Mandatory):**
   - After the key is created, click **Edit API Key** (or click on the key name).
   - Under **API restrictions**, select **Restrict key**.
   - In the dropdown, search for and select **Places API (New)**.
   - Click **Save**.
4. Copy the restricted key and save it for the next step.

#### B. Calendar OAuth 2.0 Client
1. Click **Create Credentials > OAuth client ID**.
2. Application type: **Web application**.
3. Name: `Personal Assistant`.
4. Authorized redirect URIs: Add `http://localhost:8000/dev-ui/`
5. Click **Create** and copy the **Client ID** and **Client Secret**.

---

## 🛠️ Environment Setup

1. In the Cloud Shell Editor, locate the `.env.example` file.
2. Right-click it and select **Duplicate** (or rename to `.env`).
3. Fill in your credentials:

```bash
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CALENDAR_CLIENT_ID="your-client-id"
GOOGLE_CALENDAR_CLIENT_SECRET="your-client-secret"
GOOGLE_PLACES_API_KEY="your-api-key"
```

---

## 🤖 Run the Agent

1. **Start the server:**
   ```bash
   adk web --allow_origins="regex:https://.*\.cloudshell\.dev"
   ```

2. **Open Web Preview:**
   - Click the **Web Preview** button (top-right of Cloud Shell terminal).
   - Select **Preview on port 8000**.

3. **Select the Agent:**
   - In the ADK UI, **select `personal_assistant` from the dropdown menu on the left sidebar** before sending your first message.

4. Finalize OAuth (Cloud Shell Specific):
   - In the chat, try to ask: "What is on my calendar?"
   - You will see an OAuth error page. Click on **"Error details"** to reveal the technical details of the failure.
   - Find the `redirect_uri` value in the error message. **Copy it**, but **only up to and including `/dev-ui/`** (e.g., `https://8000-xxxx.cloudshell.dev/dev-ui/`). Do not copy anything after /dev-ui/.
   - Go back to your **OAuth client ID** in the GCP Console.
   - Add that exact URI to the **Authorized redirect URIs** list.
   - **Wait 1 minute**, refresh the agent page, click on **"New session"** to start a fresh chat, and try again!
---

## 🤝 Authors

- **Hasan Rafiq** - [LinkedIn](https://www.linkedin.com/in/hrfq/)

## 💡 Customization

Edit `config.py` to change:
- `DEFAULT_LOCATION`: Your city
- `MIN_RATING`: Filter for places (default: 4.0)
- `TIMEZONE`: e.g., "Europe/Warsaw" or "America/New_York"

---

## 🧪 Example Prompts
- "Find a highly rated Italian restaurant in Warsaw."
- "What times am I free this Friday?"
- "Book a table at [Restaurant Name] for Friday at 7pm for 90 minutes."

---

## 🛑 Troubleshooting

- **403 Forbidden:** Ensure you used the `--allow_origins` flag when running `adk web`.
- **Redirect URI Mismatch:** Make sure the URI in the GCP console matches exactly what the error page showed (including the trailing `/`).
- **OAuth Popup Blocked:** If the authorization window doesn't appear, check your browser's pop-up blocker.

---

### Alternative: Local Machine Setup
*(Expand this only if you are not using Cloud Shell)*
<details>
<summary>View Local Setup Instructions</summary>

1. Install Python 3.9+ and gcloud CLI.
2. Clone repo and setup `.venv`.
3. Set `GOOGLE_APPLICATION_CREDENTIALS`.
4. Run `adk web` and access `http://localhost:8000`.
</details>
