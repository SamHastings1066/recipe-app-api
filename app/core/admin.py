"""Django admin customization"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# If you change the language of django it happens automatically.
from django.utils.translation import gettext_lazy as _

# Import all the custom models that we want to register with Django admin
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    # Order the users by id
    ordering = ['id']
    # List only the email and name fields in the suer display
    list_display = ['email', 'name']
    # we customize the fieldsets variable and only specify fields that exist
    # in our model.
    fieldsets = (
        # we pass in None for the Title of the section, but you can add a
        # string like "Title"
        (None, {'fields':('email', 'password')}),
        (
          _('Permissions'),
          {
            'fields': (
              'is_active',
              'is_staff',
              'is_superuser',
            )
          }
        ),
        (_('Important dates'), {'fields':('last_login',)}),
    )
    # make the last_login filed read only so it cannot be modified in the
    # admin
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
          'classes': ('wide',), # 'classes' key allows you to add custom css
          'fields': (
            'email',
            'password1',
            'password2',
            'name',
            'is_active',
            'is_staff',
            'is_superuser',
          ),
        }),
    )


# register the user model with our custom user admin class
admin.site.register(models.User, UserAdmin)
