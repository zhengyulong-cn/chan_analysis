<script lang="ts" setup>
import { getFuturesListWarningApi } from "@/api/modules";
import FuturesMonitorTable from "@/components/FuturesMonitorTable.vue";
import { futuresProductList } from "@/global/constants/futures";
import { IFuturesMonitorTable } from "@/global/monitorType";
import { ref, computed, onMounted, watch } from "vue";
import { ElMessage } from "element-plus";
import dayjs from "dayjs";
const tableData = ref<IFuturesMonitorTable>([]);
const lastUpdatedAt = ref<null | string>(null);
const isLoading = ref(false);
let timer: number | undefined = undefined;
onMounted(() => {
  const futuresWarning = localStorage.getItem("futuresWarning");
  if (!futuresWarning) return;
  const parsedData = JSON.parse(futuresWarning);
  tableData.value = parsedData.data;
  lastUpdatedAt.value = parsedData.lastUpdatedAt;
  timer = window.setInterval(
    () => {
      getFuturesListWarning();
    },
    1000 * 60 * 5
  );
});
const handleUpdateClick = () => {
  window.clearInterval(timer);
  getFuturesListWarning();
  timer = window.setInterval(
    () => {
      getFuturesListWarning();
    },
    1000 * 60 * 5
  );
};
const getFuturesListWarning = () => {
  isLoading.value = true;
  getFuturesListWarningApi(futuresProductList.map((el) => el.value))
    .then((res) => {
      const data = res.data as IFuturesMonitorTable;
      const currentTime = dayjs().format("YYYY-MM-DD HH:mm:ss");
      tableData.value = data;
      lastUpdatedAt.value = currentTime;
      localStorage.setItem(
        "futuresWarning",
        JSON.stringify({
          lastUpdatedAt: currentTime,
          data: tableData.value,
        })
      );
      ElMessage.success("获取开平仓监控数据成功");
    })
    .catch((err) => {
      ElMessage.error("获取开平仓监控数据失败");
      console.error(err);
    })
    .finally(() => {
      isLoading.value = false;
    });
};
const getClassifiedTableData = (tableData: IFuturesMonitorTable) => {
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
        direct: sameDirectItem.a1Direct,
        warnType: classifiedItem.warnType,
      });
    }
  }
  return operateList;
};
const classifiedList = computed(() => {
  return getClassifiedTableData(tableData.value);
});
const sameDirectList = computed(() => {
  return getSameA1AndA2DirectData(tableData.value);
});
const operateList = computed(() => {
  return getOperateList(classifiedList.value, sameDirectList.value);
});
watch(operateList, (newList) => {
  Notification.requestPermission().then((result) => {
    if (result === "granted") {
      newList.length > 0 &&
        new Notification("开平仓预警", {
          body: `【${newList.map((el) => el.symbolName).join("、")}】有开仓/平仓机会`,
        });
    }
  });
});
</script>

<template>
  <div class="pageBox">
    <header class="headerMenu">
      <div>最近更新时间：{{ lastUpdatedAt ?? "无记录" }}</div>
      <el-icon class="refresh" size="24" @click="handleUpdateClick"><Refresh /></el-icon>
    </header>
    <section class="bodySection">
      <div class="futuresMonitorTable">
        <FuturesMonitorTable :table-data="tableData" :loading="isLoading" />
      </div>
      <div class="warningWrapper">
        <div class="condition">
          <div v-if="classifiedList.length > 0" v-loading="isLoading">
            <div v-for="(item, index) in classifiedList" :key="index">
              {{ item.symbolName }}({{ item.symbol }}) - {{ item.stage }} -
              {{ item.warnType === 1 ? "做多/平空" : "做空/平多" }}
            </div>
          </div>
          <div v-else>无</div>
          <div v-if="sameDirectList.length > 0" v-loading="isLoading">
            <div v-for="(item, index) in sameDirectList" :key="index">
              {{ item.symbolName }}({{ item.symbol }})-{{
                item.directText === 1 ? "上涨" : "下跌"
              }}趋势
            </div>
          </div>
          <div v-else>无</div>
        </div>
        <div class="arrowDownIcons">
          <el-icon><Bottom /></el-icon>
          <el-icon><Bottom /></el-icon>
        </div>
        <div class="warningResult" v-loading="isLoading">
          <h2 class="title">A0级别开仓/平仓信号</h2>
          <div v-if="operateList.length > 0">
            <div v-for="(item, index) in operateList" :key="index">
              {{ item.symbolName }}({{ item.symbol }}) -
              {{ item.directText === 1 ? "上涨" : "下跌" }}趋势 -
              {{ item.warnType === 1 ? "做多/平空" : "做空/平多" }}
            </div>
          </div>
          <div v-else>无</div>
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="less" scoped>
.pageBox {
  background-color: var(--el-bg-color);
  border-radius: 1rem;
  padding: 1rem;
  max-height: calc(100% - 2rem);
  max-width: calc(100% -2rem);
  height: calc(100% - 2rem);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  row-gap: 1rem;
  .headerMenu {
    display: flex;
    flex-direction: row;
    column-gap: 1rem;
    .refresh {
      cursor: pointer;
    }
  }
  .bodySection {
    display: flex;
    flex-direction: row;
    height: inherit;
    column-gap: 1rem;
    width: 100%;
    .futuresMonitorTable {
      flex: 2;
      overflow: auto;
    }
    .warningWrapper {
      flex: 1;
      display: flex;
      flex-direction: column;
      row-gap: 0.5rem;
      .condition {
        display: flex;
        flex-direction: row;
        column-gap: 0.5rem;
        height: 25rem;
        & > div {
          flex: 1;
          border: 1px solid red;
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
        .title {
          font-size: 1.5rem;
          font-weight: bold;
        }
      }
    }
  }
}
</style>
