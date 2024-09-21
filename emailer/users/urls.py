from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_email/', views.create_email, name='create_email'),
    path('email_list/',views.email_list, name='email_list')
]

