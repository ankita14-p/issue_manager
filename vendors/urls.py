from django.urls import path
from . import views
 
urlpatterns= [
   path("vendors/",views.vendors,name="vendors"),
   path('vendors/create/', views.create_vendor, name='create_vendor'),
 ]