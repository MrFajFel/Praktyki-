

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Computer, User, Class

# Register your models here.
@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom', 'users')
    list_filter = ('classroom', 'name')

    def users(self, obj):
        count = obj.users.count()
        if count > 0:
            url = (reverse('admin:app_user_changelist') + f'?computer__id__exact={obj.id}')
            return format_html('<a href="{}">Użytkownicy ({})</a>', url, count)
        return ''

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'last_reported', 'computer')
    list_filter = ('computer', 'last_reported')
    ordering = ('-last_reported',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
