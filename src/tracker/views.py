from django.shortcuts import render
from .util import getJSON,getTimeline,getTopCountryHistory,topCountries,upload
from .models import Livedata
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

class Chartdata(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request,*args,**kwargs):
        data = {
            "dead": getTimeline('dead'),
            "recovered": getTimeline('recovered'),
            "confirmed": getTimeline('confirmed'),
            "date": getTimeline('date'),
            "topcountry": getTopCountryHistory('country'),
            "topcountry_confirmed": getTopCountryHistory('confirmed'),
            "confirmed_labels": list(range(0,70)) 
        }
        return Response(data)



def home(request,*args,**kwargs):
    # upload()
    return render(request,"index.html",{
        'records': Livedata.objects.values() ,
        'hotspots': topCountries()
        
    })
