import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import imaplib
import base64
import os
import email

# Create your views here.

# def verify(request):
#     email_user = "syndsms@gmail.com"
#     email_pass = "syndqwertyuiop09"

    # mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    # mail.login(email_user, email_pass)
    # mail.select('Inbox')
    #
    # type, data = mail.search(None, 'ALL')
    # mail_ids = data[0]
    # id_list = mail_ids.split()
    # print(id_list)
    #
    # first_email_id = int(id_list[0])
    #
    # for num in data[0].split():
    #     typ, data = mail.fetch(num, '(RFC822)')
    #     raw_email = data[0][1]
    #
    # raw_email_string = raw_email.decode('utf-8')
    # email_message = email.message_from_string(raw_email_string)
    #
    # print(email_message)
from django.views.decorators.csrf import csrf_exempt

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "syndsms" + ORG_EMAIL
FROM_PWD = "syndqwertyuiop09"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

# def readmail():
#
# # mail reading logic will come here !!
#
# # -------------------------------------------------
# #
# # Utility to read email from Gmail Using Python
# #
# # ------------------------------------------------

def read_email_from_gmail(request):
    # try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    # for i in range(latest_email_id, first_email_id, -1):
    typ, data = mail.fetch(str(latest_email_id), '(RFC822)')

    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_subject = msg['subject']
            email_from = msg['from']

            print('From : ' + email_from + '\n')
            print('Subject : ' + email_subject + '\n')
            body = msg.get_payload(decode=True)
            body_string = body.decode('utf-8')
            body_code = body_string.split(".")
            body_sender = body_code[0].split("+")
            body_sender = body_sender[1].split(" ")
            print(body)
            print(body_code)
            print(body_code[2])
            print("sender: ", body_sender[0])
            print('\n')


    # except (Exception,e):
    #     print(Exception.message)

    return HttpResponse("<h2>verification</h2>")

@csrf_exempt
def create_uudi_hash(request):
    id = None
    if(request.method == "POST"):
        id = uuid.uuid4() if request.POST.get("uuid") == "?" else None

        print(id)
    json = {
        'uuid': id
    }

    return JsonResponse(json)