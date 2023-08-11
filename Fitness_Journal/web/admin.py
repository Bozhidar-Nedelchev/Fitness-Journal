from django.contrib import admin


from .models import ProgressPhoto
from ..app_auth.models import AppUser
from django.contrib.auth.admin import UserAdmin



class FitnessProgressInline(admin.StackedInline):
    model = ProgressPhoto
    extra = 1


class AppUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email',)  # Add the field(s) you want to enable search

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    inlines = [FitnessProgressInline]

    ordering = ('email',)


admin.site.register(AppUser,AppUserAdmin)
admin.site.site_header = 'Fitness Journal Admin'
admin.site.site_title = 'Fitness Journal Admin'


