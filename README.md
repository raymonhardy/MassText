# Mass Text Message Python App

A Mass text message application using Twilio account and a gmail account. Twilio is used to grab phone provider. The gmail account is used to send SMS text messages via email. It will save you a little money on Twilio to not use a phone number they create for use and cost per message. Please follow the instructions below to set up.

# SetUp

1. Twilio

   - First create a free Twilio account https://www.twilio.com/try-twilio
   - Find your "account sid" and your "authentication token" in the settings in Twilio
   - Place your "account sid" and "authentication token" into the TwilioCreds.txt text file

   ```
   account sid
   authentication token
   ```

2. Gmail

   - Then create a free gmail account https://accounts.google.com/signup/v2/webcreateaccount?hl=en&flowName=GlifWebSignIn&flowEntry=SignUp
   - Turn off lese secure access within the google settings for the email account. https://support.google.com/accounts/answer/6010255?hl=en
   - Note the username and password
   - Place the username and password into the EmailCreds.txt like below

   ```
   username
   password
   ```

3. Numbers.csv

   - Place the list of numbers, each new number will have a new line

   ```
   801111111
   801111111
   ```

4. Text.txt

   - Add the text message to send to the recipient/s

5. Run the Application

   - Make sure you have python3 installed
   - Install Twilio
     `pip install twilio`
   - Run CMC.py
     `python3 CMD.py`
