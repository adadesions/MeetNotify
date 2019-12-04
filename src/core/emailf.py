import html2text
import quopri
import imaplib
import email
import re
import base64


def gmailContent(raw_text):
    catching = False
    raw_body = ''

    for i, line in enumerate(raw_text):
        if any(word in line for word in ['text/html', 'base64']):
            catching = True
            continue
        elif 'multipart/related' in line:
            break

        if catching:
            isKeep = any(word in line for word in ['MIME', '-==='])
            if not isKeep:
                raw_body += line

    plain_text = base64.b64decode(raw_body).decode('utf-8')

    return plain_text


def getEmailContent(raw_mail):
    match_lines = []
    for i, line in enumerate(raw_mail):
        if "body" in line:
            match_lines.append(i)

    try:
        start_line = match_lines[0] + 1
        end_line = match_lines[1]
        email_body = raw_mail[start_line:end_line]
    except IndexError:
        body_text = gmailContent(raw_mail)
        return body_text

    h2t = html2text.HTML2Text()
    raw_text = h2t.handle(' '.join(email_body))
    decoded_line = ''

    for line in raw_text.split('\n'):
        decode_text = quopri.decodestring(line).decode('iso-8859-11')

        if len(decode_text) > 0:
            decoded_line += decode_text + '\n'
        else:
            continue

    return decoded_line


def parse_uid(data):
    pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')
    match = pattern_uid.match(data)
    return match.group('uid')


def move_mail(email, password, to_folder):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email, password)
    imap.list()
    # Out: list of "folders" aka labels in gmail.
    imap.select("inbox", readonly=False) # connect to inbox.
    result, data = imap.search(None, "ALL")
    
    ids = data[0] # data is a list. (string)
    id_list = ids.split() # ids is a space separated string (list) 1 2 3 => ['1', '2', 3']
    try:
        latest_email_id = id_list[-1] # get the latest
    except IndexError:
        print('No new mail was found!')
        imap.close()
        return False

    res, data = imap.fetch(latest_email_id, "(UID)") # fetch the email body (RFC822) for the given ID
    msg_uid = parse_uid(data[0].decode('utf-8'))

    result = imap.uid('MOVE', msg_uid, to_folder)

    if result[0] == "OK":
        print('Successfully moving email')
    else:
        print('ERROR: Can not move email')
    
    imap.close()

    return True


def subjectHandler(subjectText):
    if 'utf-8' in subjectText:
        temp_subject = subjectText.split('?')[-2]
        return base64.b64decode(temp_subject).decode('utf-8')
    else:
        return subjectText


def convert2GTM7(strTime):
    time = strTime.split(' ')[-2]
    (hh, mm, ss) = time.split(':')
    hh = (int(hh)+7)%12
    strHH = str(hh)

    if len(strHH) == 1:
        strHH = '0'+strHH

    gtm7Time = ':'.join([strHH, mm, ss])

    return gtm7Time