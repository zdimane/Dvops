from django.contrib import admin
from .models import Brand, Rate, Order, Customer,Category,Product



class AdminProduct(admin.ModelAdmin):
    list_display = ["name", "price", "brand", "gender", "size", "category"]

class AdminCategory(admin.ModelAdmin):
    list_display = ["id", "type1", "type2"]

class AdminCustomer(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone", "password"]

class AdminOrder(admin.ModelAdmin):
    list_display = ["product", "customer", "quantity", "price", "adress", "phone", "date", "status"]

class AdminRate(admin.ModelAdmin):
    list_display = ["rating", "product", "customer"]

class AdminBrand(admin.ModelAdmin):
    list_display = ["brand_name", "image", "category"]

# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Category, AdminCategory)
admin.site.register(Order, AdminOrder)
admin.site.register(Rate, AdminRate)
admin.site.register(Brand, AdminBrand)