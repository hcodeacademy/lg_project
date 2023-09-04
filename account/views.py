from .models import GeneratedPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .utils import *

from django.http import FileResponse
from django.views import View
from django.shortcuts import render

from django.template.loader import get_template
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

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.lib import colors

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
    except Exception:
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



def generate_pdf(request, user_id, name):
    try:
        user = UserAccount.objects.get(id=user_id)
    except UserAccount.DoesNotExist as e:
        return redirect('account:homepage')
    pdf_name = generate_random_name(name)
    img_name = get_qrcode_image(request)
    img_path = get_image_full_path(img_name)
    #pdf buffer reader
    buffer = make_pdf(img_path, user)

    #save to model
    pdf_model = GeneratedPDF(title=user.first_name)
    pdf_model.pdf_file.save(f'{pdf_name}.pdf', buffer)
    file_path = settings.MEDIA_ROOT + '/documents/' +name+'/pdf/' + pdf_name + '.pdf'
    #download file
    response = download_pdf(file_path, user)
    buffer.seek(0)
    buffer.close()
    return response