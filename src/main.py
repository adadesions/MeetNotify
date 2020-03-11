import poplib
import imaplib
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

    # IMAP4
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(USER, PASSWORD)
    imap.select("inbox", readonly=False)

    # list items on server
    resp, items, octets = server.list()

    # Read keywords from bank
    with open("src/bank.json", 'r', encoding='utf-8') as file:
        words_bank = json.load(file)
        all_words = [ *words_bank['thai'], *words_bank['eng'] ]


    # download the multi message and convert to human readable
    # limit only last 5 mails
    items.reverse()
    limit5 = items[:5]

    for item in limit5:
        # # convert list to Message object
        msg = convert2msg(item, server)

        # Filtering
        print(all_words)
    
        isSubjectMatch = any(f in msg['subject'] for f in all_words)
        isBodyMatch = any(f in msg['bodyContent'] for f in all_words)
        # End Filtering

        print(isSubjectMatch)
        print(isBodyMatch)


        if isSubjectMatch or isBodyMatch:
            full_text = {
                'from': msg['message']['From'],
                'subject': msg['subject'],
                'date': msg['message']['Date'],
                'thai-time': msg['thaiTime'], 
                'body': msg['bodyContent']
            }

            keyword = ''.join(['(SUBJECT ', '"', full_text['subject'], '")'])
            keyword = keyword.encode('utf-8')
            print("keyword:", keyword)

            is_new = False

            try:
                result_search, data_search = imap.search(None, keyword)
                print(result_search, data_search, len(data_search[0]))
                if len(data_search[0]) > 0:
                    ids = data_search[0].split()
                    print('ids:', ids)
                    for id in ids:
                        res, data = imap.fetch(id, "(UID)") # fetch the email body (RFC822) for the given ID
                        msg_uid = emailf.parse_uid(data[0].decode('utf-8'))
                        result = imap.uid('MOVE', msg_uid, 'Meeting')
                    is_new = True
            except:
                print("Exception IMAP4: Can't read subject")
                # raise


            if is_new:
                # Output message
                print(full_text)
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
                print('Sent Notification')
                # End Line Notification
        else:
            print('No match emails or No new mails in mailbox')


if __name__ == '__main__':
    main()
