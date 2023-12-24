from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

model_list = [Publisher, Author, Book]
admin.site.register(model_list)