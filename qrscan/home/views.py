import random
import string
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
import qrcode as q
import qrcode.image.svg
from .models import qrcode

def generate_QR_Id():
    chars=string.ascii_lowercase + string.digits
    size=10
    qr_id = ''.join(random.choice(chars) for _ in range(size))
    return 'qr_' + qr_id

def encrypt(text,s=2):
    result = ""
    for i in range(len(text)):
      char = text[i]
      if (char.isupper()):
         result += chr((ord(char) + s-65) % 26 + 65)
      elif char.isdigit() or char == '_':
         result += char
      else:
         result += chr((ord(char) + s - 97) % 26 + 97)
    return result

def decrypt(text, s=2):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) - s - 65) % 26 + 65)
        elif char.isdigit() or char == '_':
            result += char
        else:
            result += chr((ord(char) - s - 97) % 26 + 97)
    return result

def home(request):
    url = "https://victoryschools.in/"
    if len(qrcode.objects.all()) == 0:
        qr_id = generate_QR_Id()
        status = '0'
        qrcode.objects.create(QR_Id = qr_id)
    else:
        last_qr = qrcode.objects.last()
        if(last_qr.Registration_Status == 0):
            qr_id = last_qr.QR_Id
            status = '0'
        else:
            qr_id = generate_QR_Id()
            status = '1'
            qrcode.objects.create(QR_Id = qr_id)
    enc_qr_id = encrypt(qr_id)
    url += '?id=' + enc_qr_id + '&status=' + status
    code = q.make(data=url,image_factory=q.image.svg.SvgImage)
    code.save(f'static/img/{qr_id}.svg')
    return render(request, 'index.html',{'QR':qr_id})