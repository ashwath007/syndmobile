import uuid
import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import imaplib
import base64
import os
import email
from verification.models import RegisteredNo

from django.views.decorators.csrf import csrf_exempt


#Setting up static variables
ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "syndsms" + ORG_EMAIL
FROM_PWD = "syndqwertyuiop09"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


#This function returns a JsonRsponse for the in comming POST Request with a key-state & value-?.
#The JsonResponse contains the state (the state in which the verification process terminated).
#It reads the uuid and the sender's phone no. from the email and saves it to the DataBase.
@csrf_exempt
def read_email_from_gmail(request):
   json = {}
   body_code = []
   phone_no = None
   state = None

   if(request.method=="POST" and request.POST.get("state")=="?"):
        # time.sleep(5)

        #Loging in to the Email
        mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('inbox')

        #Collecting mail ids
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0]) #First mail recieved in the inbox
        latest_email_id = int(id_list[-1]) #The Recent mail in the inbox


        typ, data = mail.fetch(str(latest_email_id), '(RFC822)')

        #Reading the contents of the Recent mail in the inbox
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
                body_sender = body_sender[1].split(" ") if len(body_code) >= 1 else None
                phone_no = body_sender[0] if body_sender is not None else None
                phone_no = phone_no[2:]


        # state :-
        #
        #     0 - The uuid is already registered (not registered)
        #     1 - The phone no already exist (not registered)
        #     2 - The data has not saved successfully (not registered)
        #     3 - The data has saved successfully (Registered)

        state = 0

        #To check whether the uuid is already present
        try:
            reg = RegisteredNo.objects.get(id=body_code[2])
        except RegisteredNo.DoesNotExist:
            reg = None

        if not reg:
            state = 1

            # To check whether the phone no. is already registered
            try:
                phone = RegisteredNo.objects.get(phone=phone_no)
            except RegisteredNo.DoesNotExist:
                phone = None


            if not phone:
                state = 2

                #To register the new user (to add the no. and uuid to the DataBase
                reg = RegisteredNo()
                reg.id = body_code[2]
                reg.phone = phone_no
                reg.name = request.POST.get('name') if request.POST.get('name') else ""
                reg.save()

                # To check whether the has been saved
                try:
                    reg = RegisteredNo.objects.get(id=body_code[2])
                except RegisteredNo.DoesNotExist:
                    reg = None

                #changing flag to "3" if the data is saved
                if reg:
                    state = 3



   json = {
        'uuid': body_code[2] if len(body_code) > 1 else None,
        'phone': phone_no,
        'state': state
   }

   return JsonResponse(json)


#This function generates and returns an uuid for every POST request with a key-uuid & value-?
@csrf_exempt
def create_uudi_hash(request):
    id = None
    if(request.method == "POST"):
        id = uuid.uuid4() if request.POST.get("uuid") == "?" else None



    json = {
        'uuid': id,
        'img': "https://surlybikes.com/uploads/bikes/_medium_image/Lowside_BK0887-2000x1333.jpg"
    }

    return JsonResponse(json)


@csrf_exempt
def is_registered(request):
    state = 0

    if(request.method=="POST" and request.POST.get('state')=='?'):

        if(request.POST.get('uuid')):

            try:
                user = RegisteredNo.objects.get(id=request.POST.get('uuid'))
            except RegisteredNo.DoesNotExist:
                user = None


            if user:
                state = 1

    json = {
        'state': state
    }

    return JsonResponse(json)