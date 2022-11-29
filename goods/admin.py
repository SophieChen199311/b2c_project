from django.contrib import admin
from .models import Goods
# Register your models here.

class GoodsModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Goods, GoodsModelAdmin)
