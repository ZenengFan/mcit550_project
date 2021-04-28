from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pageTwo/', views.pageTwo, name='pageTwo'),
    path('pageThree/', views.pageThree, name='pageThree'),
    path('pageFour/', views.pageFour, name='pageFour'),
]