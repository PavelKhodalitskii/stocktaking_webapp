from django.shortcuts import render
from django.http import HttpResponse
from .createreports import create_report

# Create your views here.
def report_view(request):
    try:
        create_report()
        return HttpResponse("Report created")
    except:
        return HttpResponse("Something went wrong")