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
time = message['Date'].split(' ')[-2]
(hh, mm, ss) = time.split(':')
hh = (int(hh)+7)%12
time = ':'.join([str(hh), mm, ss])

full_text = {
    'from': message['From'],
    'subject': subject,
    'date': message['Date'],
    'thai-time': time, 
    'body': bodyContent
}
print(full_text)

# Moving Email
is_new = emailf.move_mail(USER, PASSWORD, 'Meeting')

if is_new:
    # Output message
    print(full_text)
