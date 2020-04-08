from django.contrib import admin

# Register your models here.
from .models import Livedata
admin.site.register(Livedata)

from .models import GlobalStats
admin.site.register(GlobalStats)

from .models import CountryConfirmedHistory
admin.site.register(CountryConfirmedHistory)