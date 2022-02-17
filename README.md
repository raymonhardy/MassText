# A mass text message project created with python

This grabs the text.txt file to what what message to send, then loops through the csv file that has each persons phone number. It then does a search on twilio database linking phone number to cell phone service provider. It then grabs the phone number and adds the cell phone service email service provider. For example search for XXXXXXXXX comes back with verizon will then add email service provider XXXXXXXXX@vtext.com.

You will need to create a twilio account. Use an email address to send from. In this case gmail is used. And download the necessary python packages.

You will need to use your own CSV file with a list of numbers. Right now it is looping through the second cell to grab the number. That will need to be configured as well.

You will also need to edit the text.txt file to send what message you want to send.

Index.py is the main file that runs the whole script.

text.txt is the file that contains the text that you want to send

test.csv is the csv file that the program runs through to grab the phone number then send to twilio

You will need to customize the email address to send from. Your unique Twilio account tokens.

I hope that works. If you have any questions let me know.

# SetUp
