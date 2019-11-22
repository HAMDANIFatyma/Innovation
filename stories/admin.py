from django.contrib import admin
from stories.models import School
from stories.models import Teacher
from stories.models import Student
from stories.models import Cases 
from stories.models import Subject
from stories.models import  Mois
from stories.models import  State
from stories.models import  Question



# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Cases)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(Mois)
admin.site.register(State)
admin.site.register(Question)