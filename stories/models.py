from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.db import models
from django.utils.html import escape, mark_safe
from django.dispatch import receiver
from django.utils import timezone
from djrichtextfield.widgets import RichTextWidget
from djrichtextfield.models import RichTextField
from django.utils.translation import ugettext_lazy 



# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class School(models.Model):
    name_school = models.CharField(max_length=30, unique=True)
    adresse_school= models.CharField(max_length=90)
    speciality_school=models.CharField(max_length=30)
    email = models.EmailField()
    premier_stop = models.TextField(max_length=200, null=True, blank=True)
    deuxieme_stop = models.TextField(max_length=200, null=True, blank=True)
    limit_stop = models.TextField(max_length=200, null=True, blank=True )
    date_premier_stop = models.DateTimeField(null=True, blank=True)
    date_deuxieme_stop = models.DateTimeField(null=True, blank=True)
    date_limit_stop = models.DateTimeField(null=True, blank=True )
    color = models.CharField(max_length=7, default='#007bff')


    def __str__(self):
        return self.name_school

    def get_html_badge(self):
        name = escape(self.name_school)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class State(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')
    
    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class Teacher(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=70,blank=True)
    first = models.CharField(max_length=25,blank=True)
    last = models.CharField(max_length=25,blank=True)
    school=models.ManyToManyField(School , related_name='teachers_schools')

   
    def __str__(self):
        return self.user.username





class Mois(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)



class Cases(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    school_case = models.ForeignKey(School, on_delete=models.CASCADE,verbose_name=u"Sélectionnez votre Etablissement", help_text=u"Add help text(School)...", related_name='cases')
    mois = models.ForeignKey(Mois, on_delete=models.CASCADE, related_name='cases_mois')
    # General Informations
    title_case = models.CharField(max_length=255, verbose_name=u"Your case name ", help_text=u"Make your title attention-grabbing and informative.", null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,verbose_name=u"Subject", help_text=u"hLe domaine...", related_name='cases_subject')
    # Produit
    produit = models.CharField(max_length=125,verbose_name=u"Le produit ", help_text=u"help text...", null=True)
    image_produit = models.ImageField(upload_to='images/',verbose_name=u"Figure associée au produit",help_text=u"help text...", null=True,blank=True)
    date = models.CharField(max_length=125,verbose_name=u"Date", help_text=u"help text...", null=True)
    context = RichTextField(null=True,verbose_name=u"Context", help_text=u"Son histoire, le contexte...")
    context_images = models.ImageField(upload_to='images/', verbose_name=u"Figure associée au contexte", help_text=u"help text...", null=True,blank=True)
    description= RichTextField(null=True, verbose_name=u"Description du produit", help_text=u"help text...")
    description_shema = models.ImageField(upload_to='images/',verbose_name=u"Figure associée à la description",help_text=u"help text...", null=True,blank=True)
    diagnostic = RichTextField(verbose_name=u"Diagnostic de la nouveauté", help_text=u"help text...", null=True)
    diagnostic_shema= models.ImageField(upload_to='images/',verbose_name=u"Figure associée à la diagnostic de la nouveauté",help_text=u"help text...", null=True,blank=True)
    # processus = models.FileField(upload_to='images/',verbose_name=u"Name", help_text=u"Please enter your name...", null=True, blank=True)
    processus = RichTextField(verbose_name=u"Description du processus d’innovation", help_text=u"help text...", null=True, blank=True)
    processus_shema = models.ImageField(upload_to='images/',verbose_name=u"Figure associée à la description du processus d’innovation", help_text=u"help text...", null=True,blank=True)
    # fin 
    reference= RichTextField(null=True,verbose_name=u"Références", help_text=u"help text...")
    abstract= RichTextField(null=True,verbose_name=u"Abstract", help_text=u"help text...")
    auteur = models.CharField(max_length=200,null=True,verbose_name=u"L(es)'auteur(s)", help_text=u"help text...")
    created_date = models.DateTimeField(default=timezone.now,verbose_name=u"date de création", help_text=u"help text...")
    published_date = models.DateTimeField(default=timezone.now,verbose_name=u"date de publication", help_text=u"help text...")
    evaluer =  models.BooleanField(default=False, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cases_state', null = True)
    def __str__(self):
        return self.title_case

    def publish(self):
        self.created_date = timezone.now()
        self.save()
 


    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=70,blank=True)
    first = models.CharField(max_length=25,blank=True)
    last = models.CharField(max_length=25,blank=True)
    school= models.ManyToManyField(School ,  related_name='students_school')

   
    def __str__(self):
        return self.user.username




class Question(models.Model):
    case = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name='questions')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='taken_quizzes', null = True)
    text = models.CharField('Question', max_length=255)
    date = models.DateTimeField(auto_now_add=True, null = True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='states', null = True)
    date_evaluation = models.DateTimeField(default=timezone.now, null = True)
    

    def __str__(self):
        return self.text

    def publish(self):
        self.date_evaluation = timezone.now()
        self.save()
    

class TakenQuiz(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='quizzes', null = True)
    quiz = models.ForeignKey(Cases, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

