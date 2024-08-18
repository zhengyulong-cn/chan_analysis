from django.views import View
from chan_core.analysis import statisticsTradeSignalWarning
from chan_core.config import KLineLevel
from chan_futures.future_product import FutureProduct
from django.http import HttpResponseForbidden
import json


def getFutureData(request):
    if request.method == "GET":
        symbol = request.GET.get("symbol")
        period = request.GET.get("period")
        if not symbol or not period:
            raise ValueError("symbol or period is empty")
        plainData = FutureProduct(
            symbol=symbol,
            period=period,
        ).getResponseData()
        return plainData
    return HttpResponseForbidden("method is not GET")


def getfuturesListWarning(request):
    if request.method == "POST":
        dict = json.loads(request.body)
        symbolList = dict["symbol_list"]
        symbolsSignalList = []
        for symbol in symbolList:
            futureProduct15 = FutureProduct(
                symbol=symbol,
                period=KLineLevel.Level_15M.value,
            )
            futureProduct60 = FutureProduct(
                symbol=symbol,
                period=KLineLevel.Level_60M.value,
            )
            a0SignalList = statisticsTradeSignalWarning(
                futureProduct15.histPrice,
                penPointList=futureProduct15.a0PenPointList,
            )
            a1SignalList = statisticsTradeSignalWarning(
                futureProduct60.histPrice,
                penPointList=futureProduct60.a0PenPointList,
            )
            symbolsSignalList.append(
                {
                    "symbol": symbol,
                    "a0Direct": (
                        1 if futureProduct15.a0PenPointList[-1]["type"] == "top" else -1
                    ),
                    "a1Direct": (
                        1 if futureProduct15.a1PenPointList[-1]["type"] == "top" else -1
                    ),
                    "a2Direct": (
                        1 if futureProduct15.a2PenPointList[-1]["type"] == "top" else -1
                    ),
                    "a0SignalList": a0SignalList,
                    "a1SignalList": a1SignalList,
                }
            )
        return symbolsSignalList
    return HttpResponseForbidden("method is not POST")
