# Outlook Meeting Scheduler Agent

This is an autonomous AI agent that connects to your Outlook calendar to schedule meetings.

## Prerequisites

1.  **Python 3.x** installed.
2.  **Microsoft Outlook Account** (Personal or Work/School).
3.  **Azure App Registration** (to get API credentials).

## Setup Instructions

### 1. Register an App in Azure Portal

To allow this script to access your calendar, you need to register an application with Microsoft:

1.  Go to the [Azure Portal App Registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps).
2.  Click **New registration**.
3.  **Name**: `OutlookSchedulerAgent` (or any name you prefer).
4.  **Supported account types**:
    *   Choose **"Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)"** if you are using a personal Outlook.com account.
    *   Choose **"Accounts in this organizational directory only"** if you are using a corporate account and your admin allows it.
5.  **Redirect URI**:
    *   Select **Public client/native (mobile & desktop)** from the dropdown.
    *   Enter: `https://login.microsoftonline.com/common/oauth2/nativeclient`
6.  Click **Register**.

### 2. Get Credentials

1.  On the **Overview** page of your new app, copy the **Application (client) ID**.
2.  (Optional) If you created a "Web" app instead of "Public client", you might need a Client Secret. Go to **Certificates & secrets** > **New client secret**. Copy the **Value**. *Note: For the setup described in step 1 (Public client), a secret is usually not required.*

### 3. Install Dependencies

Open your terminal in this directory and run:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set your Client ID (and Secret if you have one) as environment variables.

**Windows (PowerShell):**
```powershell
$env:OUTLOOK_CLIENT_ID="your-client-id-here"
# Only if you have a secret:
# $env:OUTLOOK_CLIENT_SECRET="your-client-secret-here"
```

**Windows (CMD):**
```cmd
set OUTLOOK_CLIENT_ID=your-client-id-here
```

**Mac/Linux:**
```bash
export OUTLOOK_CLIENT_ID="your-client-id-here"
```

### 5. Run the Agent

```bash
python agent.py
```

## Usage

1.  When you run the script for the first time, it will generate a **URL**.
2.  Copy and paste this URL into your browser.
3.  Log in with your Microsoft account and grant permissions.
4.  The browser will redirect to a blank page (or the redirect URI). **Copy the full URL** from the address bar of that blank page.
5.  Paste the URL back into the terminal prompt.
6.  The agent will then:
    *   Authenticate.
    *   Check if 9:00 AM IST today is free.
    *   Create a meeting with subject "Test".
    *   Confirm the creation.

## Troubleshooting

*   **"Reply URL does not match"**: Ensure you added `https://login.microsoftonline.com/common/oauth2/nativeclient` as a **Mobile and desktop applications** redirect URI in the Azure Portal > Authentication tab.
*   **Timezone issues**: The script is hardcoded to use `Asia/Kolkata` (IST). You can change this in `agent.py` if needed.
