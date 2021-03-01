from django.shortcuts import render,redirect
from django.views import View
from app.forms import *
from django.contrib import messages
from app.decorators import student_login_check
from django.utils.decorators import method_decorator
from django.db import connection

# Create your views here.



class ApplyView(View):
    def return_render_file(self,request):
        courses = CourseCategory.objects.all()
        student_id = request.session['student_id']
        student = Student.objects.get(id=student_id)
        choose_courses = ChooseCourse.objects.filter(student=student)
        context = {
                'student':student,
                'choose_courses':choose_courses,
                'courses':courses
            }
        
        return render(request,"app/apply.html",context)
    
    @method_decorator(student_login_check)
    def get(self,request):
        
            
        return self.return_render_file(request)
    
    @method_decorator(student_login_check)
    def post(self,request):
        all_data = dict(request.POST)
        print(all_data)
        all_data.pop('csrfmiddlewaretoken')
        student = Student.objects.get(id=request.session['student_id'])
        count_course = 0
        for key,value in all_data.items():
            if value[0]:
                course = CourseCategory.objects.get(id=int(key))
                add_course = ChooseCourse(course_cat=course,student=student,priority=int(value[0]))
                add_course.save()

                count_course +=1
        
        if count_course<1:
            messages.error(request,"please choose atleast one course")
            return redirect("apply")
        
        return self.return_render_file(request)


class StudentLogin(View):

    def get(self,request):
        try:
            request.session['student_id']
            return redirect("apply")
        except:
            form = StudentLoginForm()
            
            context = {'form':form}
            return render(request,"app/student_login.html",context)
    
    def post(self,request):
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            request.session['student_id']=student.id
            return redirect("apply")
        else:
            messages.error(request,"roll no or birth date not exists")
        return redirect("student_login")
@student_login_check
def logout(request):
    del request.session['student_id']
    return redirect("student_login")



    
   

    
