<script lang="ts" setup>
import { futuresProductList } from "@/global/constants/futures";
import { IFuturesMonitorTable } from "@/global/monitorType";
import { computed, PropType, watch } from "vue";

const props = defineProps({
  tableData: {
    type: Array as PropType<IFuturesMonitorTable>,
    required: true,
  },
  loading: {
    type: Boolean,
  },
});
const getSmallAdjustmentsList = (tableData: IFuturesMonitorTable) => {
  const classifiedList: any[] = [];
  for (const item of tableData) {
    const a0SignalList = item.a0SignalList;
    const product = futuresProductList.find((el) => el.value === item.symbol)!;
    const symbolName = product.label;
    const a0Direct = item.a0Direct;
    const a1Direct = item.a1Direct;
    const a2Direct = item.a2Direct;
    const currentCrossType = a0SignalList[a0SignalList.length - 1].crossType;
    if (a0Direct === a1Direct && a1Direct === a2Direct) {
      if (a0Direct === 1 && currentCrossType === 1) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          direct: a0Direct,
          warnType: 1,
        });
      }
      if (a0Direct === -1 && currentCrossType === -1) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          direct: a0Direct,
          warnType: -1,
        });
      }
    }
  }
  return classifiedList;
};
const getClassifiedList = (tableData: IFuturesMonitorTable) => {
  const classifiedList: any[] = [];
  for (const item of tableData) {
    const a0SignalList = item.a0SignalList;
    const product = futuresProductList.find((el) => el.value === item.symbol)!;
    const symbolName = product.label;
    let currentCrossType = a0SignalList[a0SignalList.length - 1].crossType;
    let currentFenxingType = a0SignalList[a0SignalList.length - 1].fenxingType;
    if (currentFenxingType !== 0) {
      const lastIdx = a0SignalList.findLastIndex((el) => el.crossType !== 0);
      if (lastIdx < 0) {
        continue;
      }
      const lastCrossType = a0SignalList[lastIdx].crossType;
      if (Math.abs(lastIdx - a0SignalList.length) < 8 && lastCrossType === currentFenxingType) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A0",
          crossType: currentCrossType,
          fenxingType: currentFenxingType,
          warnType: currentFenxingType,
        });
      }
    }
    if (currentCrossType !== 0) {
      const lastIdx = a0SignalList.findLastIndex((el) => el.fenxingType !== 0);
      if (lastIdx < 0) {
        continue;
      }
      const lastFenxingType = a0SignalList[lastIdx].fenxingType;
      if (Math.abs(lastIdx - a0SignalList.length) < 8 && lastFenxingType === currentCrossType) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A0",
          crossType: currentCrossType,
          fenxingType: currentFenxingType,
          warnType: currentCrossType,
        });
      }
    }
    const a1SignalList = item.a1SignalList;
    currentCrossType = a1SignalList[a1SignalList.length - 1].crossType;
    currentFenxingType = a1SignalList[a1SignalList.length - 1].fenxingType;
    if (currentFenxingType !== 0) {
      const lastIdx = a1SignalList.findLastIndex((el) => el.crossType !== 0);
      if (lastIdx < 0) {
        continue;
      }
      const lastCrossType = a1SignalList[lastIdx].crossType;
      if (Math.abs(lastIdx - a1SignalList.length) < 8 && lastCrossType === currentFenxingType) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A1",
          crossType: currentCrossType,
          fenxingType: currentFenxingType,
          warnType: currentFenxingType,
        });
      }
    }
    if (currentCrossType !== 0) {
      const lastIdx = a1SignalList.findLastIndex((el) => el.fenxingType !== 0);
      if (lastIdx < 0) {
        continue;
      }
      const lastFenxingType = a1SignalList[lastIdx].fenxingType;
      if (Math.abs(lastIdx - a1SignalList.length) < 8 && lastFenxingType === currentCrossType) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A1",
          crossType: currentCrossType,
          fenxingType: currentFenxingType,
          warnType: currentCrossType,
        });
      }
    }
  }
  return classifiedList;
};
const getSameA1AndA2DirectData = (tableData: IFuturesMonitorTable) => {
  const sameDirectList: any[] = [];
  for (const item of tableData) {
    const product = futuresProductList.find((el) => el.value === item.symbol)!;
    const symbolName = product.label;
    if (item.a1Direct === item.a2Direct) {
      sameDirectList.push({
        symbol: item.symbol,
        symbolName: symbolName,
        direct: item.a1Direct,
      });
    }
  }
  return sameDirectList;
};
const getOperateList = (classifiedList, sameDirectList) => {
  const operateList: any[] = [];
  for (const sameDirectItem of sameDirectList) {
    const classifiedItem = classifiedList.find(
      (el) => el.symbol === sameDirectItem.symbol && el.stage === "A0"
    );
    if (classifiedItem) {
      operateList.push({
        symbol: sameDirectItem.symbol,
        symbolName: sameDirectItem.symbolName,
        direct: sameDirectItem.direct,
        warnType: classifiedItem.warnType,
      });
    }
  }
  return operateList;
};
const classifiedListList = computed(() => {
  return getClassifiedList(props.tableData);
});
const sameDirectList = computed(() => {
  return getSameA1AndA2DirectData(props.tableData);
});
const operateList = computed(() => {
  return getOperateList(classifiedListList.value, sameDirectList.value);
});
const smallAdjustmentsList = computed(() => {
  return getSmallAdjustmentsList(props.tableData);
});
watch(operateList, (newList) => {
  Notification.requestPermission().then((result) => {
    if (result === "granted") {
      newList.length > 0 &&
        new Notification("标准开平仓信号", {
          body: `【${newList.map((el) => el.symbolName).join("、")}】有开仓/平仓机会`,
        });
    }
  });
});
watch(smallAdjustmentsList, (newList) => {
  Notification.requestPermission().then((result) => {
    if (result === "granted") {
      newList.length > 0 &&
        new Notification("加仓信号", {
          body: `【${newList.map((el) => el.symbolName).join("、")}】有加仓机会`,
        });
    }
  });
});
const getWarnTypeText = (direct: number, warnType: number) => {
  if (direct === 1) {
    return warnType === 1 ? "做多" : "平多";
  }
  if (direct === -1) {
    return warnType === 1 ? "平空" : "做空";
  }
  return "-";
};
</script>

<template>
  <div class="warningWrapper">
    <div class="condition">
      <div class="sameDirectBox" v-loading="loading">
        <h2 class="title">A1和A2级别同向</h2>
        <div v-if="sameDirectList.length > 0">
          <div v-for="(item, index) in sameDirectList" :key="index">
            {{ item.symbolName }}({{ item.symbol }})-{{ item.direct === 1 ? "上涨" : "下跌" }}趋势
          </div>
        </div>
        <div v-else>无</div>
      </div>
      <div class="standardAdjustmentsBox" v-loading="loading">
        <h2 class="title">MACD金死叉+强势顶底分型信号</h2>
        <div v-if="classifiedListList.length > 0">
          <div v-for="(item, index) in classifiedListList" :key="index">
            {{ item.symbolName }}({{ item.symbol }}) - {{ item.stage }} -
            {{ item.warnType === 1 ? "做多/平空" : "做空/平多" }}
          </div>
        </div>
        <div v-else>无</div>
      </div>
    </div>
    <div class="arrowDownIcons">
      <el-icon><Bottom /></el-icon>
      <el-icon><Bottom /></el-icon>
    </div>
    <div class="warningResult" v-loading="loading">
      <h2 class="title">A0级别标准开仓/平仓信号</h2>
      <div v-if="operateList.length > 0">
        <div v-for="(item, index) in operateList" :key="index">
          {{ item.symbolName }}({{ item.symbol }}) - {{ item.direct === 1 ? "上涨" : "下跌" }}趋势 -
          {{ getWarnTypeText(item.direct, item.warnType) }}
        </div>
      </div>
      <div v-else>无</div>
    </div>
    <div class="warningResult" v-loading="loading">
      <h2 class="title">A0次级别回调加仓信号（趋势延续性点位）</h2>
      <div v-if="smallAdjustmentsList.length > 0">
        <div v-for="(item, index) in smallAdjustmentsList" :key="index">
          {{ item.symbolName }}({{ item.symbol }}) -
          {{ item.direct === 1 ? "上涨" : "下跌" }}趋势延续 -
          {{ getWarnTypeText(item.direct, item.warnType) }}
        </div>
      </div>
      <div v-else>无</div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.warningWrapper {
  display: flex;
  flex-direction: column;
  row-gap: 0.5rem;
  height: 100%;
  .title {
    font-size: 1.5rem;
    font-weight: bold;
    font-family: "Kaiti";
  }
  .condition {
    display: flex;
    flex-direction: row;
    column-gap: 0.5rem;
    height: 25rem;
    & > div {
      flex: 1;
      border: 1px solid;
      border-radius: 0.5rem;
      padding: 0.5rem;
      overflow: auto;
    }
  }
  .arrowDownIcons {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    height: 1.5rem;
  }
  .warningResult {
    flex: 1;
    border: 1px solid red;
    border-radius: 0.5rem;
    padding: 0.5rem;
    overflow: auto;
  }
}
</style>
