from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Student)
admin.site.register(ChooseCourse)
admin.site.register(SelectionOnCourse)
