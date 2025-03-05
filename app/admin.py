from django.contrib import admin
from .models import post,comment,like,profile
admin.site.register(post)
admin.site.register(comment)
admin.site.register(like)
admin.site.register(profile)

