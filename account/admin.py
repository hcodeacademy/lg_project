from django.contrib import admin
from account.models import UserAccount

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','state_of_origin', 'created_at']
    list_filter = ['created_at']

admin.site.register(UserAccount, UserAdmin)

