from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','chat_id','name','address','phone','mobile')

admin.site.register(Customer,CustomerAdmin)
