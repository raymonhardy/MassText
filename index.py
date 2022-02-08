
# Import smtplib for the actual sending function
# go to C:\Users\raymon.hardy\AppData\Local\Programs\Python\Python36-32\Scripts then:
# pip install beautifulsoup4, pip install lxml, pip install twilio, pip install phonenumbers
import re
import os
import csv
import smtplib
import string
from twilio.rest import Client
import sys
print(sys.path)


# to run file go into terminal. Go the the directory that this file is in and run python index.py

# Reads in Text File that contains the text message/ returns the text in a string
def readTextFile():
    file = open("text.txt", "r")
    Text = file.read()
    return Text


# reads the CSV file that is saved by excel returns a list
def readCSV():
    numbers = []
    f = open('<CSV File>')
    csv_f = csv.reader(f)
    # a for loop that saves each number as a sting in a list
    for row in csv_f:
        numbers.append(row[1])
    f.close()
    return numbers

    # Sends an Email from google server


def sendEmail(From, To):
    newTo = attachEmailProvider(To)
    if(newTo != "reg espression not met " and newTo != "couldn't find carrier"):
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.ehlo()
        smtp.starttls()
        smtp.login('<email>', '<password>')
        # gets the string from the text file
        Text = readTextFile()
        # smtp.sendmail(From, newTo , Text)
        smtp.quit()
    else:
        print("couldn't find provider or carrier")


# Used to find the carrier number. Costs $0.005 per lookup
def twilio(To):
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "<token>"
    auth_token = "<token>"
    client = Client(account_sid, auth_token)

    number = client.lookups.phone_numbers(To).fetch(
        type="carrier",
    )

    return (number.carrier['name'])


# uses conditional statements to find the carrier and attaches appropriate @ to it
def attachEmailProvider(cTo):
    # regex = r"(\d{3})-(\d{3})-(\d{4})"
    regex = r'.'
    if(re.search(regex, cTo)):
        m = re.match(regex, cTo)
        # To = (m.group(1)+m.group(2)+m.group(3))
        To = m
        # carrier = twilio(To)
        carrier = twilio(cTo)
        # use a regresssion to make sure that it is a 7 digit phone number
        if carrier == 'Verizon Wireless':
            return (To+'@vtext.com')
        if carrier == 'Alltel Wireless':
            return (To+'@messag.alltel.com')
        if carrier == 'AT&T Wireless':
            return (To+'@txt.att.net')
        if carrier == 'Boost Mobile Wireless':
            return (To+'@sms.bluecell.com')
        if carrier == 'Sprint Wireless':
            return (To+'@sms.bluecell.com')
        if carrier == 'T-Mobile USA, Inc.':
            return (To+'@tmomail.net')
        if carrier == 'U.S. Cellular Wireless':
            return (To+'@email.uscc.net')
        if carrier == 'Virgin Mobile Wireless':
            return (To+'@vmobl.com')
        if carrier == 'Republic Wireless Wireless':
            return (To+'@text.republicwireless.com')
        else:
            print("couldn't find carrier: " + carrier)
            return ("couldn't find carrier")
    else:
        print("reg expression not met")
        return("reg espression not met ")


# Calls each function
def main():
    # Can only have 160 characters
    mainEmail = '<email>'
    listOfNumbers = readCSV()

    # runs through the numbers list and then calls sendEmail
    for i in listOfNumbers:
        sendEmail(mainEmail, i)
        print(i)


main()
