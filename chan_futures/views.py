from django.views import View
from chan_futures.future_product import FutureProduct
from django.http import HttpRequest


class FuturesView(View):
    def get(self, request: HttpRequest):
        symbol = request.GET.get("symbol")
        period = request.GET.get("period")
        if not symbol or not period:
            raise ValueError("symbol or period is empty")
        plainData = FutureProduct(
            symbol=symbol,
            period=int(period),
        ).getPlainData()
        return plainData
