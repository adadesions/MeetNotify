import poplib
import string, random
import io
import email
import logging
import core.emailf as emailf
import quopri
import base64
import requests
import json

from email.parser import Parser

SERVER = "pop.gmail.com"
USER  = "malunthakesr@gmail.com"
PASSWORD = "#tot#8899"
URL = 'https://notify-api.line.me/api/notify'  # เป็น url ที่เราจะ request
TOKEN = 'ufNNz3vfTEZxwiXImGbDjGKAoPwEaFhS9ApJSVELS6m'  # token เป็นตัวที่ gen ออกมาได้จากการขอ token ในหน้าเว็บของ line
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+TOKEN}  # เป็นการกำหนด header


def convert2msg(obj, server):
    # download the first message in the list
    id, size = obj.decode('utf-8').split(" ")
    print('=== Email Information ===')
    print("id: ", id, " size: ", size)
    resp, text, octets = server.retr(id)

    # # convert list to Message object
    text = '\n'.join([t.decode('utf-8') for t in text])
    raw_mail = text.split('\n')
    bodyContent = emailf.getEmailContent(raw_mail)
    message = Parser().parsestr(text)
    subject = emailf.subjectHandler(message['Subject'])
    thaiTime = emailf.convert2GTM7(message['Date'])

    msg = {
        'subject': subject,
        'bodyContent': bodyContent,
        'message': message,
        'thaiTime': thaiTime
    }

    return msg


def main():
    # connect to server
    logging.debug('connecting to ' + SERVER)
    server = poplib.POP3_SSL(SERVER)

    # log in
    server.user(USER)
    server.pass_(PASSWORD)

    # list items on server
    resp, items, octets = server.list()

    # Multiple items
    # for item in items:
    #     msg = convert2msg(item, server)
    #     print(msg)

    # single item
    msg = convert2msg(items[-1], server)
    print(msg['subject'])



if __name__ == '__main__':
    main()
