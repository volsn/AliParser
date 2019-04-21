from django.contrib import admin
from .models import Seller, Product
from django.contrib.auth.models import Group

admin.site.site_header = '1668 Parser'

class ProductAdmin(admin.ModelAdmin):
    exclude = ('Num', )

admin.site.register(Seller)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(Group)
