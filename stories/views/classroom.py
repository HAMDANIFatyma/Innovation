from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.utils import timezone
from django.utils.translation import ugettext



class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:stories_list')
        else:
            return redirect('students:students_borad')
    return render(request, 'classroom/home.html')

   
