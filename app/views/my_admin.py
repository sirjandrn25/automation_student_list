from django.shortcuts import render,redirect
from django.views import View
from app.forms import *
from app.models import *
from django.db import connection



class AdminHome(View):
    def get(self,request):
        
        return render(request,"admin_base/index.html")



class ViewStudent(View):
    def get(self,request):
        students = Student.objects.all()
        context = {
            'students':students
        }

        return render(request,"my_admin/view_student.html",context)




class UpdateStudent(View):
    def get(self,request,student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return redirect("view_student")
        form = StudentForm(instance=student)
        context = {
            'form':form
        }
        return render(request,"my_admin/update_student.html",context)

    def post(self,request,student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return redirect("view_student")
        form = StudentForm(instance=student,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_student")

        context = {
            'form':form
        }
        return render(request,"my_admin/update_student.html",context)






class AddStudent(View):
    def get(self,request):
        form = StudentForm()
        context = {
            'form':form
        }
        return render(request,"my_admin/add_student.html",context)
    
    def post(self,request):
        form = StudentForm(request.POST)
        
        if form.is_valid():
            students = Student.objects.all()
            student = form.save(commit=False)
            student.roll_no = "ioe-2077-"+str(students.count()+1)
            student.save()

            return redirect("add_student")
        context = {
            'form':form
        }
        return render(request,"my_admin/add_student.html",context)



def get_student_applications(request):
   
    choose_course_list = []
    with connection.cursor() as cursor:
        cursor.execute(f"select distinct C.student_id from app_choosecourse as C where C.student_id not in(select selection.student_id from app_selectiononcourse as selection)")
        rows = cursor.fetchall()
        students=[]
        for row in rows:
            student = Student.objects.get(id=row[0])
            students.append(student)
            

        
    for student in students:
        choose_courses = ChooseCourse.objects.filter(student=student)
        print(choose_courses)
        with connection.cursor() as cursor:
            cursor.execute(f"select C.course_cat_id from app_choosecourse as C where C.student_id={student.id} order by C.priority")
            choose_courses = []
            for row in cursor.fetchall():
                course = CourseCategory.objects.get(id=row[0])
                print(course)
                choose_courses.append(course)
            print(choose_courses)

            if choose_courses:
                new_item = {}
                new_item['student']=student
                new_item['courses']=choose_courses
                choose_course_list.append(new_item)
    context = {
        'choose_course_list':choose_course_list
    }
    
    
    return render(request,"my_admin/admission_application.html",context)

class AdmissionApplication(View):

    def get(self,request):
        
        return get_student_applications(request)


class SelectionList(View):
    def get(self,request):
        selections = SelectionOnCourse.objects.all()
        try:
            course_id = request.GET['search_by_course']
            if course_id:
                with connection.cursor() as cursor:
                    cursor.execute(f"select S.id from app_selectiononcourse as S where S.course_id = {course_id}")
                    temp = []
                    for row in cursor.fetchall():
                        temp.append(SelectionOnCourse.objects.get(id=row[0]))
                    print(temp)
                    selections=temp
                        
                    
        except:
            pass
        courses = CourseCategory.objects.all()
        context = {
            'selections':selections,
            'courses':courses
        }
        return render(request,"my_admin/selection_list.html",context)

    


class GenerateResult(View):

    def get(self,request):
        student_with_Courses = []
        
        with connection.cursor() as cursor:
            cursor.execute("select C.student_id from app_choosecourse as C,app_student as S where C.student_id=S.id and C.student_id not in(select student_id from app_selectiononcourse) group by C.student_id order by S.rank")
        
            for row in cursor.fetchall():
                temp_dict = {}
                temp_dict['student_id'] =row[0]
                temp_dict['courses'] = []
                cursor.execute(f"select C.id from app_choosecourse as C where C.student_id={row[0]} order by C.priority")
                for course_id in cursor.fetchall():
                    temp_dict['courses'].append(course_id[0])
                student_with_Courses.append(temp_dict)
        self.select_by_course(*student_with_Courses)
                
        return get_student_applications(request)

    def select_by_course(self,*args):
        student_with_courses = list(args)
        for item in student_with_courses:
            student = Student.objects.get(id=item['student_id'])
            for choose_id in item['courses']:
                choose_object = ChooseCourse.objects.get(id=choose_id)
                if student.tribe:
                    if self.add_tribe_on_course(choose_object):
                        break
                elif student.gender == "male":
                    if self.add_on_course(choose_object):
                        break
                elif student.gender =="female":
                    if self.add_girl_on_course(choose_object):
                        break

                    
    
    
    def add_girl_on_course(self,choose_object):
        course = choose_object.course_cat
        girl_remaining_seat = 0
        with connection.cursor() as cursor:
            cursor.execute(f"select count(*) from app_selectiononcourse as selection,app_student as S where selection.course_id = {course.id} and S.id=selection.student_id and S.gender='female'")
            row = cursor.fetchone()
            
            if row[0]<course.girl_seat:
                selection = SelectionOnCourse(course=course,student=choose_object.student,girl_priorty=True)
                selection.save()
                choose_object.select=True
                choose_object.save()
                return True
            else:
                return self.add_on_course(choose_object)

    
    def add_tribe_on_course(self,choose_object):
        course = choose_object.course_cat
        tribe_remaining_seat = 0
        print(course)
        with connection.cursor() as cursor:
            cursor.execute(f"select count(*) from app_selectiononcourse as selection,app_student as S where selection.course_id = {course.id} and S.id=selection.student_id and S.tribe")
            row = cursor.fetchone()
            if row[0]<course.tribe_seat:
                selection = SelectionOnCourse(course=course,student=choose_object.student,tribe_priority=True)
                selection.save()
                choose_object.select=True
                choose_object.save()
                return True
            else:
                return self.add_on_course(choose_object)



        


    def add_on_course(self,choose_object):
        print("no select")
        course = choose_object.course_cat
        remaining_other_seat = 0
        with connection.cursor() as cursor:
            cursor.execute(f"select count(*) from app_selectiononcourse as selection where selection.course_id={course.id}")
            row = cursor.fetchone()
            remaining_other_seat = row[0]
            
        
        if remaining_other_seat<course.other_seat:
            selection = SelectionOnCourse(course=course,student=choose_object.student)
            selection.save()
            choose_object.select=True
            choose_object.save()
            return True
        else:
            return False




# class EditSelection(View):
#     def get(self,request,pk):
#         try:
#             selection = SelectionOnCourse.objects.get(pk=pk)
#         except SelectionOnCourse.DoesNotExist:
#             return redirect("student_selections")
#         form = SelectionForm(instance=selection)
#         context = {
#         'form':form
#         }
#         return render(request,"my_admin/update_student.html",context)
#     def post(self,request,pk):
#         try:
#             selection = SelectionOnCourse.objects.get(pk=pk)
#         except SelectionOnCourse.DoesNotExist:
#             return redirect("student_selections")
#         form = SelectionForm(instance=selection)
#         if form.is_valid():
#             form.save()

#         return render(request,"my_admin/update_student.html",context)