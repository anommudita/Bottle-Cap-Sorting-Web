from django.urls import path
from autoBCS import views

urlpatterns = [
    # route to login page
    path('', views.user_login, name='user_login'),

    # route to logout page
    path('logout', views.user_logout, name='user_logout'),

    # route to dashboard page
    path('dashboard', views.dashboard, name='dashboard'),
]