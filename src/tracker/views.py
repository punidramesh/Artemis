from django.shortcuts import render
from tracker.utils import getData, uploadToDb
from .models import Livedata
def home(request):
    uploadToDb.upload()
    context = getData.contextPass()
    context = context[0:11]
    hotspots = getData.topCountries()
    return render(request,"index.html",{'records': context, 'hotspots': hotspots})
