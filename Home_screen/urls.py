from django.urls import path
from . import views
from .views import AddressView

urlpatterns =[
    path('',views.index, name = 'index'),
    path('home/',views.home,name='home'),
    #path('signup',views.signup, name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('map/',AddressView.as_view(),name='location'),
    #path('map/',views.map, name='map'),
    path('statistics/',views.statistics,name='statistics'),
    path('registermeter/',views.registerMeter,name='registermeter'),

]
