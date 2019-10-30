import yagmail

yag = yagmail.SMTP('your@gmail.com', 'password')
contents = """
    I have wrote this email for testing Gmail srvices!
    Yagmail is an instant service of Gmail...
"""
yag.send(
    to='sendToMail@live.com',
    subject='TOT Today',
    contents=contents,
)
