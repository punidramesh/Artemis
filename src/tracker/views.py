from django.shortcuts import render
from tracker.utils.getData import getJSON
def home(request):
    getJSON()
    return render(request,"index.html",{})
