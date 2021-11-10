from django.contrib import admin
from django.contrib.admin.decorators import display
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', )
    search_fields = ('name', 'email')
    readonly_fields = ('password',)
