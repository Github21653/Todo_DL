from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

from api.views import RegisterView,LoginView, TaskView, DeleteAllTaskView, LogoutView
urlpatterns = [
    #refresh jwt
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #apis urls
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/tasks/', TaskView.as_view()),
    path('api/tasks/<int:pk>/', TaskView.as_view()),
    path('api/tasks/delete-all/', DeleteAllTaskView.as_view()),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    #for html pages
    path('', views.index, name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register-page'),
    path('tasks/', TemplateView.as_view(template_name='tasks.html'), name='tasks-page'),

]