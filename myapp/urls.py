from django.urls import path
from . import views
#from . import file_log

urlpatterns = [
    path('',views.index, name='index'),
    #path('hai/', views.export, name='export')
    path('hai/', views.export, name="hai")
]
