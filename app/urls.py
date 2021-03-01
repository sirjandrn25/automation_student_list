from django.urls import path
from app.views.student import *
from app.views.my_admin import *
from app.views.course import *


urlpatterns = [
    path("",AdminHome.as_view(),name="admin_index"),
    path("add_student/",AddStudent.as_view(),name="add_student"),
    path("update_student/<int:student_id>/",UpdateStudent.as_view(),name="update_student"),
    path("view_student/",ViewStudent.as_view(),name="view_student"),
    path("student_selections/",SelectionList.as_view(),name="student_selections"),
    path("course_view/",CourseView.as_view(),name="course_view"),
    path("course_delete/<int:pk>/",deleteCourse,name="course_delete"),

    path('course_update/<int:pk>/',UpdateCourseView.as_view(),name="course_update"),
    path('course_category/',CourseCategoryView.as_view(),name="course_category"),
    path('course_category_update/<int:pk>/',UpdateCourseCategoryView.as_view(),name="course_category_update"),
    path('course_category_delete/<int:pk>/',deleteCourseCategory,name="course_category_delete"),

    path('admission_application/',AdmissionApplication.as_view(),name="admission_application"),
    path('generate_result/',GenerateResult.as_view(),name="generate_result"),
    path("apply/",ApplyView.as_view(),name="apply"),
    path('student_login/',StudentLogin.as_view(),name="student_login"),
    path('student_logout/',logout,name="student_logout")
  
]
