from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Events, Subtitle

# class UserAdmin(BaseUserAdmin):
#     list_display = ('phone_number', 'first_name', 'last_name', 'is_staff', 'is_active')
#     search_fields = ('phone_number', 'first_name', 'last_name')
#     ordering = ('phone_number',)
#     fieldsets = (
#         (None, {'fields': ('phone_number', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2'),
#         }),
#     )

# admin.site.register(User, UserAdmin)

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('subtitle', 'content', 'video_link')
    search_fields = ('subtitle', 'content__title')
    list_filter = ('content',)


