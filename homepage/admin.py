from django.contrib import admin

# Register your models here.
from .models import Exam, Section, Question

admin.site.register(Exam)
admin.site.register(Section)
admin.site.register(Question)
