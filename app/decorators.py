from django.shortcuts import redirect
from django.contrib import messages


def student_login_check(any_func):
    def wrapper(request):
        try:
            request.session['student_id']
            return any_func(request)
        except:
            messages.error(request,"first login required")
            return redirect("student_login")

    return wrapper

