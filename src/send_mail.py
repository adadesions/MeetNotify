import yagmail

sender_email = 'rama92.ayodhya@gmail.com'
receiver_email = 'malunthakesr@gmail.com'
passwd = '#tot#8899'

data = {
    'thai': {
        'subject': 'การนัดประชุม',
        'body': [
            'การนัดประชุมกับฝ่ายพัฒนาซอฟแวร์',
            'เรื่อง การพัฒนาโปรแกรมจัดการ MailBox',
            'ครั้งที่ 2 ประจำวันที่ 5 ธันวาคม พ.ศ. 2562'
        ]
    },
    'eng': {
        'subject': 'Urgent meeting with software team',
        'body': [
            'Dear Development team,',
            'We need some help from the team about new requirement which we received from an financial user',
            'Please visit us at ROOM 39',
            'duration: 15.00 - 17.00 pm',
            'date: 5th december 2019'
        ]
    },
    'out': {
        'subject': 'This is a spam mail',
        'body': [
            'Dear User,',
            'We need some help from the team about new requirement which we received from an financial user',
            'Please visit us at ROOM 39',
            'duration: 15.00 - 17.00 pm',
            'date: 5th december 2019'
        ]
    }
}


def single_mail(subject, contents):
    yag = yagmail.SMTP(sender_email, passwd)

    yag.send(
        to=receiver_email,
        subject=subject,
        contents=contents,
    )

    print('Status: Completely Sent to {}'.format(receiver_email))


if __name__ == '__main__':
    thai_mail = data['thai']
    eng_mail = data['eng']
    out_mail = data['out']

    # single_mail(thai_mail['subject'], thai_mail['body'])
    single_mail(eng_mail['subject'], eng_mail['body'])
    # single_mail(out_mail['subject'], out_mail['body'])
