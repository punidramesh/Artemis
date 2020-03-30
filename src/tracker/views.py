from django.shortcuts import render
from tracker.utils import getData, uploadToDb
from .models import Livedata
def home(request):
    uploadToDb.upload()
    context = getData.contextPass()
    return render(request,"index.html",{'records': context})
