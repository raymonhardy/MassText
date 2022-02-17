# Mass Text Message Python App

A Mass text message application using a free Twilio account and a free gmail account. Twilio is used to grab phone provider. The gmail account is used to send SMS text messages via email. It will save you a little money on Twilio to not use a phone number they create for use and cost per message. Please follow the instructions below to set up. Twilio give you $15 for free to use. Each phone number searched cost $.005 to search.

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
