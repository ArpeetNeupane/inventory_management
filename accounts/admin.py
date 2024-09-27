from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

#customizing form during user creation in admin interface
class CustomUserAdmin(UserAdmin):
    #form shown for existing user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    #fieldsets used for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    #list of fields to be used while displaying the User model
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

# Registering the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)