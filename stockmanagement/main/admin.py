from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Branch)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Store)
admin.site.register(Sale)
admin.site.register(Storeitem)

