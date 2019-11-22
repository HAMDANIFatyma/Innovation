from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from stories.models import (Cases, School, Student, User, Teacher, Question)
from django.forms import ModelChoiceField
from django.forms import ModelMultipleChoiceField
from django.forms import ModelForm
from django.utils.translation import ugettext



class TeacherSignUpForm(UserCreationForm):
    
    
    Schools = forms.ModelMultipleChoiceField(
        queryset=School.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
   
 
    class Meta(UserCreationForm.Meta):
        model = User
      
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.school.add(*self.cleaned_data.get('Schools'))
        return user


class StudentSignUpForm(UserCreationForm):
    Schools = forms.ModelMultipleChoiceField(
        queryset=School.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.school.add(*self.cleaned_data.get('Schools'))
        return user


class GroupForm(ModelForm):
    class Meta:
       model = Cases
       fields = ['title_case', 'subject', 'produit', 'context', 'description', 'description_shema', 'processus']



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'state', 'date_evaluation',  )




