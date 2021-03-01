from django import forms
from .models import *



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('fname','lname','birth_date','gender','address','email','rank','tribe')
        widgets = {
            'fname':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
            'lname':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            'birth_date':forms.DateInput(attrs={'class':'form-control','placeholder':'yyyy-mm-dd'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
            'rank':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Rank'}),
            'tribe':forms.CheckboxInput(attrs={'class':'custom-control custom-checkbox'})
        }


class ChooseCourseForm(forms.ModelForm):
    class Meta:
        model = ChooseCourse
        fields = ('course_cat',)
    
        widgets = {
            
            'course_cat':forms.Select(attrs={'class':'custom-select custom-select-sm'})
        }

class StudentLoginForm(forms.Form):
    ioe_roll_no = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ioe-2077-2'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"class":'form-control','placeholder':'yyyy-mm-dd'}))


    def clean(self):
        roll_no = self.cleaned_data['ioe_roll_no']
        birth_date = self.cleaned_data['birth_date']
        if roll_no and birth_date:
            try:
                student = Student.objects.get(roll_no=roll_no,birth_date=birth_date)
            except Student.DoesNotExist:
                raise forms.ValidationError("roll no or birth date doesn't exist")
        self.cleaned_data['student'] = student

        return self.cleaned_data


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name','year')
        widgets = {
        'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Course Name'}),
        'year':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Course Duration'})
        }

# girl_seat = models.IntegerField(default=0)
#     tribe_seat = models.IntegerField(default=0)
#     other_seat = models.IntegerField()
#     total_fee = models.FloatField()
#     course

class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ('f_type','girl_seat','tribe_seat','other_seat','total_fee','course')
        widgets = {
        'f_type':forms.Select(attrs={'class':'form-control','placeholder':'choose course type '}),
        'girl_seat':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter girl_seat'}),
        'other_seat':forms.NumberInput(attrs={"class":'form-control','placeholder':'Enter normal seat'}),
        'tribe_seat':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Tribe Seat'}),
        'total_fee':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Total Fee'}),
        'course':forms.Select(attrs={'class':'form-control','placeholder':'choose course'})
        }


# class SelectionForm(forms.ModelForm):
#     class Meta:
#         model = SelectionOnCourse
#         fields = ('student','course')
#         widgets = {
#         'student':forms.Select(attrs={'class':'form-control'}),
#         'course':forms.Select(attrs={'class':'form-control'})
#         }