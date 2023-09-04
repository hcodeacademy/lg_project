from django.contrib import admin
from account.models import UserAccount, GeneratedPDF

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','state_of_origin', 'created_at']
    list_filter = ['created_at']

admin.site.register(UserAccount, UserAdmin)

class PDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(GeneratedPDF, PDFAdmin)