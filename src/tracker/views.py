from django.shortcuts import render
from tracker.utils import getData, uploadToDb
def home(request):
    getData.getJSON()
    uploadToDb.upload()
    return render(request,"index.html",{})
