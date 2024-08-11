import akshare as ak
import pandas as pd
from chan_core.config import KLineLevel
from chan_core.analysis import (
    getMA,
    getOperateDirection,
    buildChanPens,
    buildChanCentral,
    MACD,
)
import numpy as np


class FutureProduct:
    symbol = ""
    period = KLineLevel.Level_15M
    histPrice: pd.DataFrame = None

    def __init__(self, symbol: str, period: KLineLevel) -> None:
        self.symbol = symbol
        self.period = period
        self.histPrice = ak.futures_zh_minute_sina(
            symbol=self.symbol,
            period=str(period),
        )
        self.analysis()

    def analysis(self):
        self.analysisMA()
        self.analysisDirect()
        self.analysisChanPens()
        self.analysisChanCentral()
        self.analysisMACD()

    def analysisMA(self):
        self.histPrice["MA5"] = getMA(self.histPrice, stage=5)
        self.histPrice["MA10"] = getMA(self.histPrice, stage=10)
        self.histPrice["MA20"] = getMA(self.histPrice, stage=20)
        self.histPrice["MA40"] = getMA(self.histPrice, stage=40)
        self.histPrice["MA80"] = getMA(self.histPrice, stage=80)
        self.histPrice["MA160"] = getMA(self.histPrice, stage=160)
        self.histPrice["MA320"] = getMA(self.histPrice, stage=320)

    def analysisMACD(self):
        macdFastLine20, macdSlowLine20, macdList20 = MACD(
            self.histPrice["close"], 10, 20, 5
        )
        self.macd20 = {
            "fastLine": macdFastLine20,
            "slowLine": macdSlowLine20,
            "macdList": macdList20,
        }
        macdFastLine80, macdSlowLine80, macdList80 = MACD(
            self.histPrice["close"], 40, 80, 20
        )
        self.macd80 = {
            "fastLine": macdFastLine80,
            "slowLine": macdSlowLine80,
            "macdList": macdList80,
        }
        macdFastLine320, macdSlowLine320, macdList320 = MACD(
            self.histPrice["close"], 160, 320, 80
        )
        self.macd320 = {
            "fastLine": macdFastLine320,
            "slowLine": macdSlowLine320,
            "macdList": macdList320,
        }

    def analysisDirect(self):
        self.histPrice["a0Direct"] = None
        self.histPrice["a1Direct"] = None
        self.histPrice["a2Direct"] = None
        for i in range(len(self.histPrice) - 1, -1, -1):
            offset = len(self.histPrice) - 1 - i
            self.histPrice.loc[i, "a0Direct"] = getOperateDirection(
                self.histPrice,
                stage=20,
                offset=offset,
            )
            self.histPrice.loc[i, "a1Direct"] = getOperateDirection(
                self.histPrice,
                stage=80,
                offset=offset,
            )
            self.histPrice.loc[i, "a2Direct"] = getOperateDirection(
                self.histPrice,
                stage=320,
                offset=offset,
            )

    def analysisChanPens(self):
        self.a0PenPointList = buildChanPens(self.histPrice, type="A0")
        self.a1PenPointList = buildChanPens(self.histPrice, type="A1")
        self.a2PenPointList = buildChanPens(self.histPrice, type="A2")

    def analysisChanCentral(self):
        self.a0CentralList = buildChanCentral(
            penPointList=self.a0PenPointList,
            bigPenPointList=self.a1PenPointList,
        )
        self.a1CentralList = buildChanCentral(
            penPointList=self.a1PenPointList,
            bigPenPointList=self.a2PenPointList,
        )

    def getPlainData(self):
        plainData = {}
        plainColumns = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            # "volume",
            # "hold",
            "MA5",
            "MA10",
            "MA20",
            "MA40",
            "MA80",
            "MA160",
            "MA320",
        ]
        histPrice = self.histPrice.loc[:, plainColumns]
        plainData["symbol"] = self.symbol
        plainData["period"] = self.period
        plainData["headers"] = plainColumns
        plainData["kLineListCount"] = histPrice.shape[0]
        # np.nan类型序列化时候需要特殊处理，转换为None才能被json序列化
        rowList = histPrice.to_dict(orient="records")
        cleanedRowList = []
        for row in rowList:
            cleanedRow = {}
            for key in row.keys():
                if type(row[key]) in [int, float] and np.isnan(row[key]):
                    cleanedRow[key] = None
                else:
                    cleanedRow[key] = row[key]
            cleanedRowList.append(cleanedRow)
        plainData["kLineList"] = cleanedRowList
        # 格式化20、80、320级别的MACD
        plainData["MACD"] = {
            "macd20": {
                "fastLine": [
                    None if np.isnan(x) else x for x in self.macd20["fastLine"]
                ],
                "slowLine": [
                    None if np.isnan(x) else x for x in self.macd20["slowLine"]
                ],
                "macdList": [
                    None if np.isnan(x) else x for x in self.macd20["macdList"]
                ],
            },
            "macd80": {
                "fastLine": [
                    None if np.isnan(x) else x for x in self.macd80["fastLine"]
                ],
                "slowLine": [
                    None if np.isnan(x) else x for x in self.macd80["slowLine"]
                ],
                "macdList": [
                    None if np.isnan(x) else x for x in self.macd80["macdList"]
                ],
            },
            "macd320": {
                "fastLine": [
                    None if np.isnan(x) else x for x in self.macd320["fastLine"]
                ],
                "slowLine": [
                    None if np.isnan(x) else x for x in self.macd320["slowLine"]
                ],
                "macdList": [
                    None if np.isnan(x) else x for x in self.macd320["macdList"]
                ],
            },
        }
        plainData["chanPens"] = {
            "a0PenPointList": self.a0PenPointList,
            "a1PenPointList": self.a1PenPointList,
            "a2PenPointList": self.a2PenPointList,
        }
        plainData["chanCentral"] = {
            "a0CentralList": self.a0CentralList,
            "a1CentralList": self.a1CentralList,
        }
        return plainData
