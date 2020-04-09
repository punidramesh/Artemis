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
        country = getData.getTopCountryHistory('country')
        country_confirmed = getData.getTopCountryHistory('confirmed')
        data = {
            "dead": dead,
            "recovered": recovered,
            "confirmed": confirmed,
            "date": date,
            "topcountry": country,
            "topcountry_confirmed": country_confirmed,
            "confirmed_labels": list(range(0,70,1)) 
        }
        return Response(data)


def home(request):
    uploadToDb.upload()
    return render(request,"index.html",{'records': getData.contextPass(),'hotspots': getData.topCountries()})
