from django.contrib import admin
from .models import Product,Transaction,Purchase


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count', 'number', 'created','image')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('total_price','number','shopper')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('transaction','product','product_count', 'total_price')
    readonly_fields = ('total_price',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Purchase,PurchaseAdmin)