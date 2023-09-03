from .models import GeneratedPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

from django.http import FileResponse
from django.views import View
from django.shortcuts import render
import os

from django.template.loader import get_template
from io import BytesIO
# from xhtml2pdf import pisay


from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import UserForm
from account.models import UserAccount
from qrcode import *
import time

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings

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
    user = None
    try:
        user = get_object_or_404(UserAccount, id=user_id)
    except Exception as e:
        return redirect('account:homepage')
    img_name = get_qrcode_image(request)
    img_path = '/media/' + img_name
    return render(request, 'user_detail.html',{'user':user, 'img_url': img_path})

def get_qrcode_image(request):
    domain = settings.DOMAIN_SITE
    qr = make(domain+request.path)
    # qr.make(fit=True)
    img_name = 'qr' + str(time.time()) + '.png'
    qr.save(settings.MEDIA_ROOT + '/' + img_name)
    return img_name

def _download_pdf(file_path, user):
    response = None
    if os.path.exists(file_path) and user != None:

        with open(file_path, 'rb') as file: 
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            file.close()
    return response


def _generate_random_name(name):
    from random import randint
    return f'{name}{randint(1,10001)}'

def _get_image_full_path(image_relative_path):
    base_dir = settings.MEDIA_ROOT
    full_path = os.path.join(base_dir, image_relative_path)
    return full_path

def _make_pdf(img_path, user):
    buffer = io.BytesIO()
    doc = canvas.Canvas(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
            name='CustomStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.black,
            leading=14,
            spaceAfter=10,
        )
    # doc.setTitle(f"{user.first_name}'s Bio Data")
    passport_image_path = user.passport.path # Replace with actual image path

        # Add content to PDF
    doc.drawImage(passport_image_path, 450, 600,  width=100, height=100)
    doc.drawString(50, 550, "Item Details: User bio data")
    doc.drawString(50, 530, f"Name: {user.first_name}")
    doc.drawString(50, 510, f"Description: {user.last_name}")
    doc.drawImage(img_path, 50, 50, width=200, height=200)

    doc.save()

    return buffer

def generate_pdf(request, user_id, name):
    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist as e:
        return redirect('account:homepage')
    pdf_name = _generate_random_name(name)
    img_name = get_qrcode_image(request)
    img_path = _get_image_full_path(img_name)
    #pdf buffer reader
    buffer = _make_pdf(img_path, user)

    #save to model
    pdf_model = GeneratedPDF(title=user.first_name)
    pdf_model.pdf_file.save(f'{pdf_name}.pdf', buffer)
    file_path = settings.MEDIA_ROOT + '/documents/' +name+'/pdf/' + pdf_name + '.pdf'
    #download file
    response = _download_pdf(file_path, user)
    buffer.seek(0)
    buffer.close()
    return response

