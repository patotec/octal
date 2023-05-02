from django.urls import path
from . import views

app_name = 'indexurl'
urlpatterns = [
	path('', views.myindex, name='index'),
	path('terms/',  views.myterm ,name='terms'),
	
	path('about-us/',  views.myabout ,name='about'),
	path('contact/',  views.mycontact ,name='contact'),
	# path('help/',  views.myhelp ,name='help'),
	


    ]

