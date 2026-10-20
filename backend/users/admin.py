from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class CampusUserAdmin(UserAdmin):
    list_display = ('email','username','matricula','is_staff','is_active')
    search_fields = ('email','username','matricula')
    fieldsets = UserAdmin.fieldsets + (('Datos academicos',{'fields':('matricula',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Datos academicos',{'fields':('email','matricula')}),)
