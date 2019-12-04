import poplib
import string, random
import io
import email
import logging
import core.emailf as emailf
import quopri
import base64

from email.parser import Parser

SERVER = "pop.gmail.com"
USER  = "malunthakesr@gmail.com"
PASSWORD = "#tot#8899"


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

        # Moving Email
        is_new = emailf.move_mail(USER, PASSWORD, 'Meeting')

        if is_new:
            # Output message
            print(full_text)
    else:
        print('No match emails or No new mails in mailbox')


if __name__ == '__main__':
    main()
