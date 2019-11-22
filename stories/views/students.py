from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from ..decorators import student_required
from ..forms import  StudentSignUpForm, GroupForm
from ..models import Cases, Student, User, School
from django.utils.translation import ugettext



class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:students_borad')



@method_decorator([login_required, student_required], name='dispatch')
class StudiesListView(ListView):
    model = Cases
    ordering = ('title_case', )
    context_object_name = 'cases'
    template_name = 'classroom/students/board/index.html'



@method_decorator([login_required, student_required], name='dispatch')
class TableListView(ListView):
    model = Cases
    ordering = ('title_case', )
    context_object_name = 'cases'
    template_name = 'classroom/students/board/tables-basic.html'

    def get_queryset(self):
        queryset = self.request.user.cases \
            .select_related('school_case') \
            .annotate(questions_count=Count('questions', distinct=True)) 
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class DatesListView(ListView):
    model = School
    context_object_name = 'cases'
    template_name ='classroom/students/board/dates.html'
    
    def get_queryset(self):
        queryset = self.request.user.student.school\
            .prefetch_related('students_school') 
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class StudiesView(ListView):
    model = Cases
    ordering = ('title_case', )
    context_object_name = 'cases'
    template_name = 'classroom/students/studies_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.cases \
            .select_related('school_case') \
            .annotate(questions_count=Count('questions', distinct=True)) 
        return queryset
#School.objects.filter(user=self.request.user)



@method_decorator([login_required, student_required], name='dispatch')
class CaseCreateView(CreateView):
    model = Cases
    fields = ('title_case', 'subject', 'state', 'produit', 'mois', 'image_produit', 'date', 'context', 'context_images', 'description', 'description_shema',  'diagnostic',  'diagnostic_shema',  'processus',  'processus_shema',  'reference', 'abstract', 'auteur', 'school_case', )
    template_name = 'classroom/students/board/forms-basic.html'
    #case_add_form

    def form_valid(self, form):
        case = form.save(commit=False)
        case.owner = self.request.user
        case.save()
        messages.success(self.request,'The stories case was created with success! Go ahead and add some questions now.')
        return redirect('students:case_change', case.pk)


@method_decorator([login_required, student_required], name='dispatch')
class CaseUpdateView(UpdateView):
    model = Cases
    fields = fields = ('title_case', 'subject', 'produit', 'mois', 'image_produit', 'date', 'context', 'context_images', 'description', 'description_shema',  'diagnostic',  'diagnostic_shema',  'processus',  'processus_shema',  'reference', 'abstract', 'auteur', 'school_case', )
    context_object_name = 'case'
    template_name = 'classroom/students/case_change_form.html'
    
    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.cases.all()

    def get_success_url(self):
        return reverse('students:case_change', kwargs={'pk': self.object.pk})



@method_decorator([login_required, student_required], name='dispatch')
class CaseDeleteView(DeleteView):
    model = Cases
    context_object_name = 'case'
    template_name = 'classroom/students/case_delete_confirm.html'
    success_url = reverse_lazy('students:studies_change_list')

    def delete(self, request, *args, **kwargs):
        case = self.get_object()
        messages.success(request, 'The case study %s was deleted with success!' % case.title_case)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.owner_studies.all()