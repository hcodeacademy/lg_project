from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import UserForm
from account.models import UserAccount
from qrcode import *
import time

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return render(request, 'user_detail.html',{'user':user})


    else:
        form = UserForm()
    return render(request, 'user_form.html',{"form":form})
        

def user_detail_view(request, user_id):
    try:
        user = get_object_or_404(UserAccount, id=user_id)
    except user.DoesNotExist as e:
        print(e)

    img_name = get_qrcode_image(request)

    return render(request, 'user_detail.html',{'user':user, 'img_name': img_name})

def get_qrcode_image(request):
    domain = settings.DOMAIN_SITE
    qr = make(domain+request.path)
    img_name = 'qr' + str(time.time()) + '.png'
    qr.save(settings.MEDIA_ROOT + '/' + img_name)
    print(img_name)
    return img_name