import re
import os
import csv
import smtplib
from twilio.rest import Client
import sys
print(sys.path)

password = Password1234!

# Reads in Text File that contains the text message/ returns the text in a string
def readTextFile(text_file):
    text_file = open(text_file, "r")
    Text = text_file.read()
    text_file.close()
    return Text


# reads the CSV file that is saved by excel returns a list
def readCSVFile(CSV_file):
    CSVlist = []
    CSV_list = open(CSV_file)
    csv_f = csv.reader(CSV_list)
    # a for loop that saves each number as a sting in a list
    for row in csv_f:
        CSVlist.append(row[0])
    CSV_list.close()
    return CSVlist


# send sms text via email
def sendSMSEmail(phoneProvider, email, email_password, recipient, text):
    if(phoneProvider != "Could not be found"):
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.ehlo()
        smtp.starttls()
        sender = email
        smtp.login(email, email_password)
        smtp.sendmail(sender, recipient, text)
        smtp.close()
    else:
        print("couldn't find provider or carrier")
    # uses conditional statements to find the carrier and attaches appropriate @ to it


# find email provider
def findEmailProvider(to, list_of_providers_array, list_of_providers_emails_array, client):
    carrier = twilioLookupByPhoneNumber(client, to)
    # carrier = 'Virgin Mobile Wireless'
    # use a regresssion to make sure that it is a 7 digit phone number
    counter = 0
    for i in list_of_providers_array:
        if carrier == i:
            provider = str(list_of_providers_emails_array[counter])
            return provider
        else:
            counter = counter+1
    else:
        return("Could not be found")


# Used to find the carrier number. Costs $0.005 per lookup
def twilioLookupByPhoneNumber(client, To):
    number = client.lookups.phone_numbers(To).fetch(
        type="carrier",
    )
    return (number.carrier['name'])


# Login into Twilio
def twilioLogin():
    # Your Account Sid and Auth Token from twilio.com/user/account
    credentials = readTextFile("TwilioCreds.txt").split('\n')
    account_sid = credentials[0]
    auth_token = credentials[1]
    client = Client(account_sid, auth_token)
    return client


# Grab email credentials
def emailInfo():
    credentials = readTextFile("EmailCreds.txt").split('\n')
    email = credentials[0]
    email_password = credentials[1]
    return email, email_password


# main function
def main():
    # Can only have 160 characters
    text = readTextFile('Text.txt')
    list_of_numbers_array = readCSVFile('Numbers.csv')
    list_of_providers_array = readCSVFile('Providers.csv')
    list_of_providers_email_array = readCSVFile('ProvidersEmails.csv')
    client = twilioLogin()
    email, email_password = emailInfo()

    # runs through the numbers list and then calls sendEmail
    for number in list_of_numbers_array:
        phone_provider = findEmailProvider(
            number, list_of_providers_array, list_of_providers_email_array, client)
        recipient = number+phone_provider
        sendSMSEmail(phone_provider, email, email_password, recipient, text)


# look for main function
if __name__ == '__main__':
    sys.exit(main())
