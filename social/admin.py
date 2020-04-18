from django.contrib import admin
from .models import Post, Like, Logger

class Post_admin(admin.ModelAdmin):
    list_display = ['aPost_text', 'nUser_id', 'id']

class Like_admin(admin.ModelAdmin):
    list_display = ['nPost_id', 'aAction', 'nUser_id']

class Logger_admin(admin.ModelAdmin):
    list_display = ['nUser_id', 'oDate', 'aAction']


admin.site.site_header = 'Social Network'
# Register your models here.

admin.site.register(Post, Post_admin)
admin.site.register(Like, Like_admin)
admin.site.register(Logger, Logger_admin)


