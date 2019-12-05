import poplib
import string, random
import io
import email
import logging
import core.emailf as emailf
import quopri
import base64
import requests

from email.parser import Parser

SERVER = "pop.gmail.com"
USER  = "malunthakesr@gmail.com"
PASSWORD = "#tot#8899"
URL = 'https://notify-api.line.me/api/notify'  # เป็น url ที่เราจะ request
TOKEN = 'ufNNz3vfTEZxwiXImGbDjGKAoPwEaFhS9ApJSVELS6m'  # token เป็นตัวที่ gen ออกมาได้จากการขอ token ในหน้าเว็บของ line
HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+TOKEN}  # เป็นการกำหนด header


def main():
    # connect to server
    logging.debug('connecting to ' + SERVER)
    server = poplib.POP3_SSL(SERVER)

    # log in
    server.user(USER)
    server.pass_(PASSWORD)

    # list items on server
    resp, items, octets = server.list()

    # download the first message in the list
    id, size = items[-1].decode('utf-8').split(" ")
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

    # Filtering 
    meetingFilter = ['Urgent', 'meeting', 'join', 'ประชุม', 'เรียกพบ', 'เข้าร่วม']
    isSubjectMatch = any(f in subject for f in meetingFilter)
    isBodyMatch = any(f in bodyContent for f in meetingFilter)
    # End Filtering

    if isSubjectMatch or isBodyMatch:
        full_text = {
            'from': message['From'],
            'subject': subject,
            'date': message['Date'],
            'thai-time': thaiTime, 
            'body': bodyContent
        }

        # Line Notification
        requests.post(
            URL,
            headers=HEADERS,
            data={
                'message': """Subject: {0}\nFrom: {1}\nDateTime: {2}\nBangkokTime: {3}\n============\n{4}"""
                    .format(full_text['subject'],
                            full_text['from'],
                            full_text['date'],
                            full_text['thai-time'],
                            full_text['body'])
            }
        )
        # End Line Notification

        # Moving Email
        is_new = emailf.move_mail(USER, PASSWORD, 'Meeting')

        if is_new:
            # Output message
            print(full_text)
    else:
        print('No match emails or No new mails in mailbox')


if __name__ == '__main__':
    main()
