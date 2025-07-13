from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Type)
admin.site.register(Monster)
admin.site.register(Material)
admin.site.register(Review)
@admin.register(Hammer)
class HammerAdmin(admin.ModelAdmin):
    list_display=('name_hammer','material','edge', 'power')
    list_editable=('power',)
    list_per_page= 10
# Register your models here.
