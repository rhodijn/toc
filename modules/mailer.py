#!/usr/bin/env python3
#
#   ###################      this module sends an email report
#   ##                 ##    version 1.0 (2025-06-10)
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##    created by rhodijn (zolo) for zhaw hsb
#   ##                 ##
#     ###################    licensed under the apache license, version 2.0
#
#===============================================================================


import smtplib, ssl

from dotenv import dotenv_values
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import *


secrets = dotenv_values('.env')


def send_email(barcode: str, processing: dict):
    """
    send an email with the enrichment report

    parameters:
    barcode: str = item barcode
    processing: dict = logging info of the currently processed record
    """
    config = load_json('config.json', 'd')

    from_email = config['email']['from']
    to_email = config['email']['to']
    password = secrets['EMAIL_PASS']

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Table of Contents Enrichment Report'
    message['From'] = from_email
    message['To'] = to_email

    if processing['mms_id']['nz'] and processing['link_tested']:
        text = f"""Enrichment Report:

Item barcode: {barcode}
MMS-ID IZ: {processing['mms_id']['iz']}
MMS-ID NZ: {processing['mms_id']['nz']}

Go to this address to see the table of contents:
{processing['url']}

Thank you for using this service!"""

        html = f"""<html>
  <body>
    <p><h2>Enrichment Report</h2>
       Item barcode: {barcode}<br />
       MMS-ID IZ: {processing['mms_id']['iz']}<br />
       MMS-ID NZ: {processing['mms_id']['nz']}<br /><br />
       Click <a href="{processing['url']}" target="_blank">here</a> to see the table of contents<br /><br />
       Thank you for using this service!
    </p>
  </body>
</html>"""
    else:
        text = f"""Enrichment Report:

Item Barcode: {barcode}
Message: {processing['messages'][-1]}

Thank you for using this service!"""

        html = f"""<html>
  <body>
    <p><h2>Enrichment Report</h2>
       Item barcode: {barcode}<br />
       Message: {processing['messages'][-1]}<br /><br />
       Thank you for using this service!
    </p>
  </body>
</html>"""

    part_1 = MIMEText(text, 'plain')
    part_2 = MIMEText(html, 'html')

    message.attach(part_1)
    message.attach(part_2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('mail.infomaniak.com', 465, context=context) as s:
        s.login(from_email, password)
        s.sendmail(from_email, to_email, message.as_string())