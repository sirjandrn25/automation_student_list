from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(default=4)
    def __str__(self):
        return self.name

faculty_choice = (
    ('regular','regular'),
    ('paid','paid')
)
class CourseCategory(models.Model):
    f_type = models.CharField(max_length=100,choices=faculty_choice)
    girl_seat = models.IntegerField(default=0)
    tribe_seat = models.IntegerField(default=0)
    other_seat = models.IntegerField()
    total_fee = models.FloatField()
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.f_type +" "+self.course.name

    def get_name(self):
        return self.f_type +" "+self.course.name



gender_choice = (
    ('male','male'),
    ('female','female')
)

class Student(models.Model):
    fname = models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=100,choices=gender_choice)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    rank = models.IntegerField()
    roll_no = models.CharField(max_length=50,default="",unique=True)
    tribe = models.BooleanField(default=False)


    def __str__(self):
        return self.fname +' '+self.lname


class ChooseCourse(models.Model):
    course_cat = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    select = models.BooleanField(default=False)
    priority = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} {self.course_cat}"
    
    class Meta:
        unique_together = ('priority','student')



class SelectionOnCourse(models.Model):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    girl_priorty = models.BooleanField(default=False)
    tribe_priority = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} {self.course}"
    
    
    




    

    

