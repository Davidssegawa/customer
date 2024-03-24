from django.urls import path
from . import views
#from .views import AddressView
from .views import MeterDataList

urlpatterns =[
    path('',views.index, name = 'index'),
    path('home/',views.home,name='home'),
    #path('signup',views.signup, name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),

    path('home/statistics/',views.statistics,name='statistics'),
    path('home/payment',views.payment, name='payment'),
    path('webhook/ttn/', views.ttn_webhook),
    path('api/meter-data/',MeterDataList.as_view(), name='meter-data-list'),
]
