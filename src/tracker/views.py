from django.shortcuts import render
from tracker.utils import getData, uploadToDb
from .models import Livedata

from rest_framework.views import APIView
from rest_framework.response import Response
class Chartdata(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request,*args,**kwargs):
        dead = getData.getTimeline('dead')
        date = getData.getTimeline('date')
        recovered = getData.getTimeline('recovered')
        confirmed = getData.getTimeline('confirmed')
        data = {
            "dead": dead,
            "recovered": recovered,
            "confirmed": confirmed,
            "date": date,
        }
        return Response(data)

def home(request):
    uploadToDb.upload()
    return render(request,"index.html",{'records': getData.contextPass(), 'hotspots': getData.topCountries()})
