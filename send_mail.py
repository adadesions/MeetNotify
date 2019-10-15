import yagmail

yag = yagmail.SMTP('5900796@go.buu.ac.th', 'phutoperjer66')
contents = """
    I have wrote this email for testing Gmail srvices!
    Yagmail is an instant service of Gmail...
"""
yag.send(
    to='59050801@go.buu.ac.th',
    subject='TOT Today',
    contents=contents,
)
