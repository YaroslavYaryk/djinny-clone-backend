from django.contrib import admin

from .models import Company, CompanyImage, BusinessStream

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyImage)
admin.site.register(BusinessStream)
