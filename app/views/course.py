from app.forms import *
from app.models import *
from django.views import View
from django.shortcuts import render,redirect


class CourseView(View):
	def get(self,request):
		courses = Course.objects.all()
		form = CourseForm()
		context = {
		'courses':courses,
		'form':form
		}

		return render(request,"my_admin/course.html",context)
	def post(self,request):
		form = CourseForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect("course_view")

class CourseCategoryView(View):
	def get(self,request):
		courses = CourseCategory.objects.all()
		form = CourseCategoryForm()
		context = {
		'courses':courses,
		'form':form
		}

		return render(request,"my_admin/course_category.html",context)
	
	def post(self,request):
		form = CourseCategoryForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect("course_category")

class UpdateCourseView(View):
	def get(self,request,pk):
		try:
			course = Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			pass
		form = CourseForm(instance=course)
		context = {
			'form':form
		}
		return render(request,"my_admin/update_course.html",context)
	
	def post(self,request,pk):
		try:
			course = Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			pass
		form = CourseForm(instance=course,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect("course_view")
		context = {
			'form':form
		}
		return render(request,"my_admin/update_course.html")

class UpdateCourseCategoryView(View):
	def get(self,request,pk):
		try:
			course = CourseCategory.objects.get(pk=pk)
		except Course.DoesNotExist:
			pass
		form = CourseCategoryForm(instance=course)
		context = {
			'form':form
		}
		return render(request,"my_admin/update_course.html",context)
	
	def post(self,request,pk):
		try:
			course = CourseCategory.objects.get(pk=pk)
		except Course.DoesNotExist:
			pass
		form = CourseCategoryForm(instance=course,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect("course_category")
		context = {
			'form':form
		}
		return render(request,"my_admin/update_course.html")

	

def deleteCourse(request,pk):
	course = Course.objects.get(id=pk)
	course.delete()
	return redirect("course_view")

def deleteCourseCategory(request,pk):
	course = CourseCategory.objects.get(pk=pk)
	course.delete()
	return redirect("course_category")





	
