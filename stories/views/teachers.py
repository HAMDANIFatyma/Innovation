from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from ..decorators import teacher_required
from ..models import Cases, Teacher, School, User, Question
from django.views.generic import CreateView, ListView, UpdateView
from ..forms import  TeacherSignUpForm, QuestionForm
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.utils.translation import ugettext



class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form_teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:stories_list')




class TeachersListView(ListView):
    model = Cases
    ordering = ('title_case', )
    context_object_name = 'cases'
    template_name = 'classroom/teachers/board/index.html'


class TableListView(ListView):
    model = Cases
    ordering = ('title_case', )
    context_object_name = 'cases'
    template_name = 'classroom/teachers/board/tables-basic.html'

    def get_queryset(self):
        teacher = self.request.user.teacher
        teacher_schools = teacher.school.values_list('pk', flat=True)
        # taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Cases.objects.filter(school_case__in = teacher_schools) 
        return queryset


 
def EvaluerlistView(request, pk):
    try:
        quiz = get_object_or_404(Cases, pk=pk)
        cases = Question.objects.filter(case__pk= quiz.pk).order_by('date')
    except Question.DoesNotExist:
        raise Http404('cases does not exist')
    
    return render(request, 'classroom/teachers/board/takens.html', context={'cases': cases})




def take_quiz(request, pk):
    quiz = get_object_or_404(Cases, pk=pk)
    teacher = request.user.teacher

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.case = quiz
            question.teacher = teacher
            question.save()
            question.case.evaluer == True
            question.case.state = question.state
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teachers:evaluer_list', quiz.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/teachers/question_add_form.html', {'case': quiz, 'form': form})



