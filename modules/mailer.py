#!/usr/bin/env python3
#
#   ##################      this module handles the upload
#   ##                ##    version 0.1 (2025-05-23)
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import smtplib, ssl

from dotenv import dotenv_values
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import *


secrets = dotenv_values('.env')


def send_mail(barcode: str, processing: dict) -> dict:
    """
    upload file to remote server (if pdf not already online)

    parameters:
    f_process: dict = {file name: dict = {}}
    f_toc: str = file name of toc
    p_bib: str = remote path to files of library (winterthur or waedenswil)
    para_file: str = path to local file

    returns:
    f_process: dict = {file name: dict = {}}
    """
    config = load_json('config.json', 'd')

    from_email = config['email']['from']
    to_email = config['email']['to']
    password = secrets['EMAIL_PASS']

    message = MIMEMultipart('alternative')
    message['Subject'] = 'multipart test'
    message['From'] = from_email
    message['To'] = to_email

    # Create the plain-text and HTML version of your message
    text = f"""\
Hi,
How are you? {barcode}
Real Python has many great tutorials:
www.realpython.com"""

    html = f"""\
<html>
  <body>
    <p>Hi,<br>
       How are you? {barcode}<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>"""

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('mail.infomaniak.com', 465, context=context) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())