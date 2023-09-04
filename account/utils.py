from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from .utils import *

from django.http import FileResponse
from django.shortcuts import render
import os



from django.conf import settings
from qrcode import *

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def download_pdf(file_path, user):
    response = None
    if os.path.exists(file_path) and user != None:

        with open(file_path, 'rb') as file: 
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            file.close()
    return response


def generate_random_name(name):
    from random import randint
    return f'{name}{randint(1,10001)}'

def get_image_full_path(image_relative_path):
    base_dir = settings.MEDIA_ROOT
    full_path = os.path.join(base_dir, image_relative_path)
    return full_path

def make_pdf(img_path, user):
    buffer = io.BytesIO()
    doc = canvas.Canvas(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
            name='CustomStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.red,
            leading=14,
            spaceAfter=10,
        )
    doc.setFont(custom_style.fontName, custom_style.fontSize)
    doc.setFillColor(custom_style.textColor)
    # doc.setTitle(f"{user.first_name}'s Bio Data")
    passport_image_path = user.passport.path # Replace with actual image path
    
        # Add content to PDF
    doc.drawImage(passport_image_path, 450, 600,  width=100, height=100)
    # add_rounded_image(doc, passport_image_path, x=450, y=600, width=100, height=100, radius=20)
    doc.drawString(50, 550, "Title: User Bio Data")

    doc.drawString(50, 530, f"Name: {user.first_name} {user.last_name}")
    doc.drawString(50, 510, f"Description: This is the bio data pdf for a user.")
    doc.drawImage(img_path, 50, 50, width=200, height=200)

    doc.save()

    return buffer