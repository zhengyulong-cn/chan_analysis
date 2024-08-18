from django.urls import path
from chan_futures.views import getFutureData, getfuturesListWarning

urlpatterns = [
    path("future_data", getFutureData),
    path("futures_list_warning", getfuturesListWarning),
]
