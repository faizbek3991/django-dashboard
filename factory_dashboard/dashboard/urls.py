from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('data/', views.data_view, name='data'),
    path('charts/', views.charts_view, name='charts'),
    path('predict/', views.predict_view, name='predict'),
]