from django.contrib import admin
from .models import User, Post, Contact

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Contact)