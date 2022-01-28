from django.contrib import admin
from .models import Building, Post, Reply, ExtendUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class BuildingAdmin(admin.ModelAdmin):
    fields = ['address', 'number_of_apts', 'city', 'state', 'creator']
admin.site.register(Building, BuildingAdmin)

class PostAdmin(admin.ModelAdmin):
    fields = ['user', 'building', 'body', 'pub_date']
admin.site.register(Post, PostAdmin)

class ReplyAdmin(admin.ModelAdmin):
    fields = ['user', 'post', 'body', 'pub_date']
admin.site.register(Reply, ReplyAdmin)

class ExtendUserInline(admin.StackedInline):
    model = ExtendUser
    can_delete = False
    verbose_name_plural = 'users'

class UserAdmin(BaseUserAdmin):
    inlines = (ExtendUserInline,)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)