from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, request




def myindex(request):
	return render(request, 'index/index.html')

def myterm(request):
	return render(request, 'index/terms.html')

def myabout(request):
	return render(request, 'index/about.html')
# def myhelp(request):
# 	return render(request, 'index/help.html')


def mycontact(request):
	if request.method == 'POST':
		form = Contactform(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Thanks for your message we will repyl you shortly')
			
	else:
		form = Contactform()
	return render(request, 'index/contact.html')
