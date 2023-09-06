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
            fontName='Times-BoldItalic',
            fontSize=16,
            textColor=colors.black,
            leading=14,
            spaceAfter=10,
        )
    heading_style = ParagraphStyle(
    name='HeadingStyle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=25,
    textColor=colors.darkblue,
    leading=20,
    spaceAfter=10,
    underline=True,
)

# Draw "USER DETAIL" heading
    doc.setFont(heading_style.fontName, heading_style.fontSize)
    doc.setFillColor(heading_style.textColor)
    doc.drawString(200, 700, "USER DETAILS")
    

    

    top_left_image_path = get_image_full_path('dark.png')
    doc.drawImage(top_left_image_path, -53, 750, width=100, height=100)

    top_right_image_path = get_image_full_path('dark.png')
    doc.drawImage(top_right_image_path, 560, 750, width=100, height=100)

    
    doc.setFont(custom_style.fontName, custom_style.fontSize)
    doc.setFillColor(custom_style.textColor)
    passport_image_path = user.passport.path

    doc.setTitle("USER DETAILS")
    doc.drawImage(passport_image_path, 65, 650,  width=100, height=100)
    holder_image_path = get_image_full_path('holder.png')
    doc.drawImage(holder_image_path, 50, 50, width=227, height=103)



    # Add content to PDF
    doc.drawImage(img_path, 350, 50, width=200, height=150)
    doc.drawString(50, 600, f"First Name: {user.first_name.capitalize()}")
    doc.drawString(350, 600, f"Last Name:{user.last_name.capitalize()}")
    doc.drawString(50, 550, f"Email:{user.email}")
    doc.drawString(350, 550, f"Gender:")
    if user.gender == 0:
        doc.drawString(410, 550, "Male")
    else:
        doc.drawString(410, 550, "Female")

    doc.drawString(50, 500, f"Local Origin: {user.local_origin.capitalize()}")
    doc.drawString(350, 500, f"State of Origin: {user.state_of_origin.capitalize()}")
    doc.drawString(50, 450, f"Occupation: {user.occupation.capitalize()}")
    doc.drawString(350, 450, f"Marital Status: ")
    if user.marital_status == 0:
        doc.drawString(460, 450, "Single")
    elif user.marital_status == 1:
        doc.drawString(460, 450, "Married")
    else:
        doc.drawString(460, 450, "Divorced")

    doc.drawString(50, 400, f"Fathers Name: {user.father_name.capitalize()} ")
    doc.drawString(350, 400, f"Mothers Name: {user.mother_name.capitalize()} ")
    doc.drawString(50, 350, f"Date Of Birth: {user.date_of_birth} ")
    doc.drawString(350, 350, f"Place Of Birth: {user.place_of_birth.capitalize()} ")
    doc.drawString(50, 300, f"Contact Address: {user.contact_address.capitalize()} ")


    doc.save()

    return buffer
