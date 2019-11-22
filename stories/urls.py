from django.urls import include, path
from .views import classroom, students, teachers



urlpatterns = [
    path('', classroom.home, name='home'),

    path('teachers/', include(([
        path('', teachers.TeachersListView.as_view(), name='stories_list'),
        path('studies/tables/', teachers.TableListView.as_view(), name='table_list'),
        path('evaluer/<int:pk>/', teachers.EvaluerlistView, name='evaluer_list'),
        path('case/<int:pk>/', teachers.take_quiz, name='take_quiz'),

        
#<int:pk>/

    ], 'stories'), namespace='teachers')),

   path('students/', include(([    
        path('', students.StudiesListView.as_view(), name='students_borad'),
        path('studies/', students.StudiesView.as_view(), name='studies_change_list'),
        path('studies/tables/', students.TableListView.as_view(), name='table_list'),
        path('studies/dates/', students.DatesListView.as_view(), name='dates_list'),
        path('case/add/', students.CaseCreateView.as_view(), name='case_add'),
        path('case/<int:pk>/', students.CaseUpdateView.as_view(), name='case_change'),
        path('case/<int:pk>/delete/', students.CaseDeleteView.as_view(), name='case_delete'),
        ], 'stories'), namespace='students')),

]

