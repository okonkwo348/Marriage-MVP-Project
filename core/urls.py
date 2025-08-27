# In core/urls.p
from django.urls import path
from . import views # <--- THIS LINE IS CRUCIAL
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/', views.course, name='course'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
    # new
    path('lesson/<int:lesson_id>/quiz/', views.quiz_page, name='quiz_page'),
    path('mentorship/', views.mentorship_booking, name='mentorship_booking'),
    path('forum/', views.forum, name='forum'),
    path('contact/', views.contact, name='contact'),
    path('support/', views.support, name='support'),
    path('assessment/', views.assessment, name='take_quiz'),
    
    # THIS IS THE MISSING/INCORRECT LINE FOR AI QUIZ GENERATION
   path('lesson/<int:lesson_id>/generate_quiz_ai/', views.generate_quiz_ai, name='generate_quiz_ai'),

]