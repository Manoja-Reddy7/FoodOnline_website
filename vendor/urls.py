from django.urls import path
from accounts import views as Accountviews

from . import views

urlpatterns = [
   path('',Accountviews.vendorDashboard),
   path('profile/',views.vprofile,name='vprofile'),
   
]

    
     