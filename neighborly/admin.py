from django.contrib import admin
from .models import Building, Post, Reply

class BuildingAdmin(admin.ModelAdmin):
    fields = ['address', 'number_of_apts']
admin.site.register(Building, BuildingAdmin)

class PostAdmin(admin.ModelAdmin):
    fields = ['user', 'building', 'body', 'pub_date']
admin.site.register(Post, PostAdmin)

class ReplyAdmin(admin.ModelAdmin):
    fields = ['user', 'post', 'body', 'pub_date']
admin.site.register(Reply, ReplyAdmin)