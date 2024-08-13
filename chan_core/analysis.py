import numpy as np
import pandas as pd
import talib
from typing import List


def getMA(histPrice: pd.DataFrame, *, stage: int):
    return talib.MA(histPrice["close"], stage)


def getOperateDirection(histPrice: pd.DataFrame, *, stage: int, offset: int):
    """
    获取当前均线方向
    """
    MAX = talib.MA(histPrice["close"], stage)
    MAX_2 = talib.MA(histPrice["close"], stage // 2)
    MAX_4 = talib.MA(histPrice["close"], stage // 4)
    compareIdx = -2 - offset
    if abs(compareIdx) > len(histPrice):
        return 0
    if (
        MAX_4.iloc[compareIdx] > MAX.iloc[compareIdx]
        and MAX_2.iloc[compareIdx] > MAX.iloc[compareIdx]
    ):
        return 1
    elif (
        MAX_4.iloc[compareIdx] < MAX.iloc[compareIdx]
        and MAX_2.iloc[compareIdx] < MAX.iloc[compareIdx]
    ):
        return -1
    return 0


def getPenMaxMinPrice(
    histPrice: pd.DataFrame,
    startIdx: int,
    endIdx: int,
    direct: int,
):
    if direct == 1:
        lowMinPrice = histPrice.iloc[startIdx:endIdx]["low"].min()
        lowMinPriceIdx = histPrice.iloc[startIdx:endIdx]["low"].idxmin()
        return {
            "price": lowMinPrice,
            "priceIdx": lowMinPriceIdx,
            "type": "buttom" if direct == 1 else "top",
            "datetime": histPrice.iloc[lowMinPriceIdx]["datetime"],
        }
    elif direct == -1:
        highMaxPrice = histPrice.iloc[startIdx:endIdx]["high"].max()
        highMaxPriceIdx = histPrice.iloc[startIdx:endIdx]["high"].idxmax()
        return {
            "price": highMaxPrice,
            "priceIdx": highMaxPriceIdx,
            "type": "buttom" if direct == 1 else "top",
            "datetime": histPrice.iloc[highMaxPriceIdx]["datetime"],
        }
    else:
        raise ValueError("direct的值不可能为0，请检查输入数据")


def buildChanPens(histPrice: pd.DataFrame, *, type: str):
    """
    根据历史价格数据和类型构建画笔

    参数:

    histPrice : pd.DataFrame 包含历史价格数据的DataFrame。

    type : str 类型标识符，可以是"A0", "A1", 或 "A2"。

    返回: penPointList 由函数计算得出的笔的点位
    """
    if type not in ["A0", "A1", "A2"]:
        raise ValueError("Type must be one of 'A0', 'A1', or 'A2'")
    mapType2Col = {
        "A0": "a0Direct",
        "A1": "a1Direct",
        "A2": "a2Direct",
    }
    directColData = histPrice[mapType2Col[type]]
    penDirect = 0
    # 笔判断条件切换的点位
    switchList = []
    for i, curDirect in enumerate(directColData):
        if curDirect == 1 and penDirect != 1:
            penDirect = 1
            switchList.append((i, penDirect))
        if curDirect == -1 and penDirect != -1:
            penDirect = -1
            switchList.append((i, penDirect))
    penList = []
    for i in range(len(switchList)):
        curSwitch = switchList[i]
        endIdx = curSwitch[0]
        direct = curSwitch[1]
        if i == 0:
            priceObj = getPenMaxMinPrice(histPrice, 0, endIdx, direct)
            penList.append(priceObj)
        else:
            lastPriceObj = penList[len(penList) - 1]
            startIdx = lastPriceObj["priceIdx"]
            priceObj = getPenMaxMinPrice(histPrice, startIdx, endIdx, direct)
            penList.append(priceObj)
        if i == len(switchList) - 1:
            lastPriceObj = penList[len(penList) - 1]
            startIdx = lastPriceObj["priceIdx"]
            priceObj = getPenMaxMinPrice(
                histPrice, startIdx, len(histPrice), direct * -1
            )
            penList.append(priceObj)
    return penList


def getNextBigPenDirect(startIdx: int, endIdx: int, bigPenPointList: list):
    for i, curPenPoint in enumerate(bigPenPointList):
        if i + 1 > len(bigPenPointList) - 1:
            continue
        nextPenPoint = bigPenPointList[i + 1]
        if curPenPoint['priceIdx'] <= startIdx and endIdx <= nextPenPoint['priceIdx']:
            if curPenPoint["type"] == "top":
                return -1
            else:
                return 1
    return 0


def buildChanCentral(*, penPointList, bigPenPointList):
    """
    根据笔绘制中枢

    参数:

    penPointList: 本级别笔

    bigPenPointList: 大一个级别笔

    返回: centralList 由函数计算得出的中枢点位
    """
    centralList = []
    for i, curPoint in enumerate(penPointList):
        if i < 3:
            continue
        second2LastPoint = penPointList[i - 1]
        third2LastPoint = penPointList[i - 2]
        fourth2LastPoint = penPointList[i - 3]
        curPointIdx = curPoint["priceIdx"]
        fourth2LastPointIdx = fourth2LastPoint["priceIdx"]
        # 大笔方向
        bigDirect = getNextBigPenDirect(
            fourth2LastPointIdx, curPointIdx, bigPenPointList
        )
        if bigDirect == 1:
            if (
                curPoint["price"] < fourth2LastPoint["price"]
                and second2LastPoint["price"] > third2LastPoint["price"]
            ):
                uppperPrice = min(second2LastPoint["price"], fourth2LastPoint["price"])
                lowerPrice = max(curPoint["price"], third2LastPoint["price"])
                newCentral = {
                    "idxRange": [
                        fourth2LastPoint["priceIdx"],
                        curPoint["priceIdx"],
                    ],
                    "timeRange": [
                        fourth2LastPoint["datetime"],
                        curPoint["datetime"],
                    ],
                    "priceRange": [lowerPrice, uppperPrice],
                    "centralDirect": bigDirect,
                }
                if not centralList:
                    centralList.append(newCentral)
                    continue
                oldCentral = centralList[len(centralList) - 1]
                # 判断x轴(坐标/时间)是否重叠
                xOverlapJudge = (
                    oldCentral['idxRange'][1] > newCentral['idxRange'][0]
                    and oldCentral['idxRange'][0] < newCentral['idxRange'][1]
                )
                # 判断y轴(价格)是否重叠
                yOverlapJudge = (
                    oldCentral['priceRange'][1] > newCentral['priceRange'][0]
                    and oldCentral['priceRange'][0] < newCentral['priceRange'][1]
                ) or (
                    oldCentral['priceRange'][0] < newCentral['priceRange'][1]
                    and oldCentral['priceRange'][1] > newCentral['priceRange'][0]
                )
                if not xOverlapJudge and not yOverlapJudge:
                    centralList.append(newCentral)
                elif not xOverlapJudge and yOverlapJudge:
                    centralList.append(newCentral)
                elif xOverlapJudge and yOverlapJudge:
                    centralList.pop()
                    newIdxRange = [
                        oldCentral['idxRange'][0],
                        newCentral['idxRange'][1],
                    ]
                    newPriceRange = [
                        oldCentral['priceRange'][0],
                        oldCentral['priceRange'][1],
                    ]
                    newTimeRange = [
                        oldCentral['timeRange'][0],
                        newCentral['timeRange'][1],
                    ]
                    mergedCentral = {
                        "idxRange": newIdxRange,
                        "timeRange": newTimeRange,
                        "priceRange": newPriceRange,
                        "centralDirect": bigDirect,
                    }
                    centralList.append(mergedCentral)
                else:
                    print("X轴重叠但Y轴不重叠，直接跳过")
        if bigDirect == -1:
            if (
                curPoint["price"] > fourth2LastPoint["price"]
                and second2LastPoint["price"] < third2LastPoint["price"]
            ):
                uppperPrice = min(curPoint["price"], third2LastPoint["price"])
                lowerPrice = max(second2LastPoint["price"], fourth2LastPoint["price"])
                newCentral = {
                    "idxRange": [
                        fourth2LastPoint["priceIdx"],
                        curPoint["priceIdx"],
                    ],
                    "timeRange": [
                        fourth2LastPoint["datetime"],
                        curPoint["datetime"],
                    ],
                    "priceRange": [lowerPrice, uppperPrice],
                    "centralDirect": bigDirect,
                }
                if not centralList:
                    centralList.append(newCentral)
                    continue
                oldCentral = centralList[len(centralList) - 1]
                # 判断x轴(坐标/时间)是否重叠
                xOverlapJudge = (
                    oldCentral['idxRange'][1] > newCentral['idxRange'][0]
                    and oldCentral['idxRange'][0] < newCentral['idxRange'][1]
                )
                # 判断y轴(价格)是否重叠
                yOverlapJudge = (
                    oldCentral['priceRange'][1] > newCentral['priceRange'][0]
                    and oldCentral['priceRange'][0] < newCentral['priceRange'][1]
                ) or (
                    oldCentral['priceRange'][0] < newCentral['priceRange'][1]
                    and oldCentral['priceRange'][1] > newCentral['priceRange'][0]
                )
                if not xOverlapJudge and not yOverlapJudge:
                    centralList.append(newCentral)
                elif not xOverlapJudge and yOverlapJudge:
                    centralList.append(newCentral)
                elif xOverlapJudge and yOverlapJudge:
                    centralList.pop()
                    newIdxRange = [
                        oldCentral['idxRange'][0],
                        newCentral['idxRange'][1],
                    ]
                    newTimeRange = [
                        oldCentral['timeRange'][0],
                        newCentral['timeRange'][1],
                    ]
                    newPriceRange = [
                        oldCentral['priceRange'][0],
                        oldCentral['priceRange'][1],
                    ]
                    mergedCentral = {
                        "idxRange": newIdxRange,
                        "timeRange": newTimeRange,
                        "priceRange": newPriceRange,
                        "centralDirect": bigDirect,
                    }
                    centralList.append(mergedCentral)
                else:
                    print("X轴重叠但Y轴不重叠，直接跳过")
    return centralList


def buildChanBuyingSellingPoints(*, penPointList, centralList, bigPenPointList):
    buyingSellingPointsList = []
    for i, bigPenPoint in enumerate(bigPenPointList):
        if i + 1 > len(bigPenPointList) - 1:
            continue
        nextBigPenPoint = bigPenPointList[i + 1]
        bigStartIdx = bigPenPoint["priceIdx"]
        bigEndIdx = nextBigPenPoint["priceIdx"]
        bigDirect = 1 if nextBigPenPoint["type"] == "top" else -1
        intervalList = []
        for curPoint in penPointList:
            curIdx = curPoint["priceIdx"]
            curPrice = curPoint["price"]
            curType = curPoint["type"]
            if bigStartIdx <= curIdx and curIdx <= bigEndIdx:
                if bigDirect == 1 and curType == "buttom":
                    if not intervalList:
                        intervalList.append(
                            {
                                "type": 1,
                                "label": "一买",
                                "priceIdx": curIdx,
                                "price": curPrice,
                                "datetime": curPoint["datetime"],
                            }
                        )
                    elif len(intervalList) == 1:
                        intervalList.append(
                            {
                                "type": 2,
                                "label": "二买",
                                "priceIdx": curIdx,
                                "price": curPrice,
                                "datetime": curPoint["datetime"],
                            }
                        )
                    else:
                        intervalList.append(
                            {
                                "type": 3,
                                "label": "三买",
                                "priceIdx": curIdx,
                                "price": curPrice,
                                "datetime": curPoint["datetime"],
                            }
                        )
                if bigDirect == -1 and curType == "top":
                    if not intervalList:
                        intervalList.append(
                            {
                                "type": -1,
                                "label": "一卖",
                                "priceIdx": curIdx,
                                "price": curPrice,
                                "datetime": curPoint["datetime"],
                            }
                        )
                    elif len(intervalList) == 1:
                        intervalList.append(
                            {
                                "type": -2,
                                "label": "二卖",
                                "priceIdx": curIdx,
                                "price": curPrice,
                                "datetime": curPoint["datetime"],
                            }
                        )
                    else:
                        intervalList.append(
                            {
                                "type": -3,
                                "label": "三卖",
                                "priceIdx": curIdx,
                                "price": curPrice,
                                "datetime": curPoint["datetime"],
                            }
                        )
        buyingSellingPointsList.append(intervalList)
    return buyingSellingPointsList


def MACD(data, fast_period=10, slow_period=20, singal_period=5):
    fastMA = talib.MA(data, fast_period)
    slowMA = talib.MA(data, slow_period)
    macdLine: List[float] = np.array(fastMA, dtype=float) - np.array(
        slowMA, dtype=float
    )
    signalLine = talib.MA(macdLine, singal_period)
    macdList = (macdLine - np.array(signalLine)) * 2
    return macdLine, signalLine, macdList


def checkMACDCross(histPrice, stage: int):
    """
    crossType为1表示金叉，为-1表示死叉，为0表示没有
    diffZeroAxis为1表示在DIFF>10时出现的，为-1表示在DIFF<-10出现的，为0表示在[-10,10]区间出现的
    """
    DIFF, DEA, _MACD = MACD(histPrice["close"], stage // 2, stage, stage // 4)
    if len(DIFF) < 2 or len(DEA) < 2:
        return (0, 0)
    latest_DIFF = DIFF[-1]
    previous_DIFF = DIFF[-2]
    latest_DEA = DEA[-1]
    previous_DEA = DEA[-2]
    crossType = 0
    diffZeroAxis = 0
    # 金叉条件
    if latest_DIFF > latest_DEA and previous_DIFF <= previous_DEA:
        crossType = 1
    # 死叉条件
    elif latest_DIFF < latest_DEA and previous_DIFF >= previous_DEA:
        crossType = -1
    else:
        crossType = 0
    if abs(latest_DIFF) <= 10:
        diffZeroAxis = 0
    else:
        if latest_DIFF < 0:
            diffZeroAxis = -1
        else:
            diffZeroAxis = 1
    return (crossType, diffZeroAxis)


def operateWarn(direct_20: int, direct_80: int, direct_320: int) -> int:
    """
    为±2表示1h和4h趋势方向一致，15min回调
    为±1表示1h和4h趋势方向一致，15min也一致或模糊，此时应该是持仓等等
    为0表示1h和4h趋势方向不一致，不操作
    """
    if direct_80 == -1 and direct_320 == -1:
        if direct_20 == 1:
            return -2
        else:
            return -1
    elif direct_80 == 1 and direct_320 == 1:
        if direct_20 == -1:
            return 2
        else:
            return 1
    else:
        return 0


def macdCrossWarn(corssType: int, diffZeroAxis: int):
    """
    为±3表示金死叉
    为2表示零轴上的金叉，为-2表示零轴下的死叉，都代表着原先趋势延续
    为±1表示零轴附近的金死叉，是弱势金死叉
    为0表示没有
    """
    if corssType == 1:
        if diffZeroAxis == -1:
            return 3
        elif diffZeroAxis == 1:
            return 2
        else:
            return 1
    elif corssType == -1:
        if diffZeroAxis == 1:
            return -3
        elif diffZeroAxis == -1:
            return -2
        else:
            return -1
    else:
        return 0
