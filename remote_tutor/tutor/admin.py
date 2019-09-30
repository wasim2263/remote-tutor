from django.contrib import admin

from .models import (College, School, Category, Subject, Department, University, Occupation)

# Register your models here.
admin.site.register(College)
admin.site.register(School)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(University)
admin.site.register(Occupation)
