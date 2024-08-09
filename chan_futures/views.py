from django.views import View
from chan_core.config import KLineLevel
from chan_futures.future_product import FutureProduct


class FuturesView(View):
    def get(self, request):
        plainData = FutureProduct(
            "SA0",
            period=str(KLineLevel.Level_15M.value),
        ).getPlainData()
        return plainData
