from django.contrib import admin

from .models import Course, Board, Topic, Post

# Register your models here.
admin.site.register(Course)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)