<<<<<<< HEAD
# Mass Text — Twilio

A small desktop app for sending an SMS message to a list of recipients through
the Twilio Messaging API. The app uses Tkinter for its interface and Twilio's
Messaging Service to deliver messages; it does not use carrier email-to-text
gateways.

## Requirements

- Python 3
- A Twilio account and configured Messaging Service
- The Python package in `requirements.txt`
- Tkinter, which is included with many Python installations (some installations
  require it to be installed separately)

## Install

From the project directory, create and activate a virtual environment, then
install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

## Configure Twilio

To find your credentials, sign in at [twilio.com/console](https://www.twilio.com/console)
and select your account. On the dashboard, look under **Account Info** for your
**Account SID** and **Auth Token**. Click **Show** or the eye icon to reveal the
token, then copy these values into `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
below. You can also find them in **Workbench → Overview → API credentials**.
Treat the Auth Token like a password; never share it or commit it to Git.
See [Twilio's credential guide](https://www.twilio.com/docs/usage/workbench).

Set these environment variables before launching the app:

- `TWILIO_ACCOUNT_SID` — your Twilio Account SID
- `TWILIO_AUTH_TOKEN` — your Twilio Auth Token
- `TWILIO_MESSAGING_SERVICE_SID` — the SID of your Twilio Messaging Service

For macOS or Linux, set them in the terminal:

```sh
export TWILIO_ACCOUNT_SID="your-account-sid"
export TWILIO_AUTH_TOKEN="your-auth-token"
export TWILIO_MESSAGING_SERVICE_SID="your-messaging-service-sid"
```

On Windows PowerShell, use `$env:NAME = "value"` for each variable. Keep the
Auth Token private; do not put credentials in source code or commit them.

## Run

With the environment variables set and the virtual environment active:

```sh
python mass_text_gui.py
```

Choose a CSV file containing one phone number in the **first column** of each
row. Do not include a header row. Use phone numbers in international format
(for example, `+14155550123`). The app displays the loaded recipients so you
can review them before sending.

Write the message and select **Send message**. The app asks for confirmation,
shows sending progress, and reports when sending finishes or if a Twilio error
stops the batch. Messages are sent one at a time.

## Estimated costs

As of November 9, 2026, Twilio lists a U.S. SMS starting rate of $0.0083 per
outbound message segment, before carrier fees and applicable taxes. At that
base rate, one single-segment message sent to 300 recipients would cost about
**$2.49** ($0.0083 x 300).

Longer messages may be split into multiple segments, increasing the per-recipient
cost. Number rental and any required A2P 10DLC registration or campaign fees are
separate. Rates and fees can change; see [Twilio's U.S. SMS pricing](https://www.twilio.com/en-us/sms/pricing/us)
for current details.

## Responsible use

Only message people who have explicitly agreed to receive your messages. Follow
Twilio's messaging policies and the laws and consent requirements that apply
to your recipients.
=======
# Mass Text Message Python App

This application is a mass text messaging tool built with Python using a free Twilio account and a free Gmail account.

Twilio is used to identify the recipient’s mobile carrier (phone provider). The Gmail account is then used to send SMS messages via email-to-SMS gateways, which can reduce messaging costs by avoiding the per-message fees associated with sending SMS directly through a Twilio phone number.

Twilio provides a $15 free trial credit when you create an account. Carrier lookup requests cost $0.005 per phone number searched.

Please follow the setup instructions below to configure the application.

# SetUp

1. Download the zip or Clone the repository
   `git clone https://github.com/raymonhardy/MassText`

2. Create Twilio Account

   - First create a free Twilio account https://www.twilio.com/try-twilio
   - Find your "account sid" and your "authentication token" in the settings in Twilio
   - Place your "account sid" and "authentication token" into the TwilioCreds.txt text file

   ```
   account sid
   authentication token
   ```

3. Create Gmail Email Account

   - Then create a free gmail account https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp
   - Turn off lese secure access within the google settings for the email account. https://support.google.com/accounts/answer/6010255?hl=en
   - Note the username and password
   - Place the username and password into the EmailCreds.txt like below

   ```
   username
   password
   ```

4. Add numbers into Numbers.csv

   - Place the list of numbers, each new number will have a new line

   ```
   801111111
   801111111
   ```

5. Add Text Message into Text.txt

   - Add the text message to send to the recipient/s

   ```
    Test Text Message
   ```

6. Install Dependencies and Run the Application

   - Make sure you have the most up-to-date python3 installed
   - Install the Twilio python package:
     `pip install twilio`
   - Run the python application with:
     `python3 CMD.py`
>>>>>>> 729a58a4bec89c032f940d041f5651883a3ba06b
