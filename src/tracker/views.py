from django.shortcuts import render
from tracker.utils import getData, uploadToDb
from .models import Livedata
def home(request):
    uploadToDb.upload()
    return render(request,"index.html",{})
