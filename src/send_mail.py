import yagmail

yag = yagmail.SMTP('rama92.ayodhya@gmail.com', '#tot#8899')
contents = """
    <body>
        I have wrote this email for testing Gmail srvices!
        Yagmail is an instant service of Gmail...
    </body>
"""
yag.send(
    to='malunthakesr@gmail.com',
    subject='Meeting urgent',
    contents=contents,
)
