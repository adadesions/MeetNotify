import yagmail

yag = yagmail.SMTP('rama92.ayodhya@gmail.com', '#tot#8899')
contents = [
        "I have wrote this email for testing Gmail srvices!",
        "Yagmail is an instant service of Gmail...",
        "ทดสอบระบบ"
]

yag.send(
    to='malunthakesr@gmail.com',
    subject='Meeting urgent(Ada)',
    contents=contents,
)
