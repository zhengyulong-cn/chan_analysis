from django.urls import path
from chan_futures.views import FuturesView

urlpatterns = [
    path("future_data/", FuturesView.as_view()),
]
