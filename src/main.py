import poplib
import string, random
import io
from email.parser import Parser
import email
import logging
import core.emailf as emailf
import quopri
import base64

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
subject = message['Subject']

if 'utf-8' in subject:
    temp_subject = subject.split('?')[-2]
    subject = base64.b64decode(temp_subject).decode('utf-8')


full_text = {
    'from': message['From'],
    'subject': subject,
    'date': message['Date'],
    'body': bodyContent
}
print(full_text)

# Moving Email
is_new = emailf.move_mail(USER, PASSWORD, 'Meeting')

if is_new:
    # Output message
    print(full_text)
