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
    })
    .catch((err) => {
      ElMessage.error("获取开平仓监控数据失败");
    })
    .finally(() => {
      isLoading.value = false;
    });
};
const getClassifiedTableData = (tableData: IFuturesMonitorTable) => {
  const classifiedList: any[] = [];
  for (const item of tableData) {
    const a0SignalList = item.a0SignalList;
    const a1anda2DirectIsSame = item.a1Direct === item.a2Direct;
    const product = futuresProductList.find((el) => el.value === item.symbol)!;
    const symbolName = product.label;
    if (a0SignalList[a0SignalList.length - 1].fenxingType !== 0) {
      const lastIdx = a0SignalList.findLastIndex((el) => el.crossType !== 0);
      if (Math.abs(lastIdx - a0SignalList.length) < 8) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A0",
          message:
            "出现MACD金死叉+强势顶底分型开仓/平仓判定" +
            (a1anda2DirectIsSame ? "【A1和A2级别趋势方向相同】" : ""),
          a1anda2DirectIsSame: a1anda2DirectIsSame,
        });
      }
    }
    if (a0SignalList[a0SignalList.length - 1].crossType !== 0) {
      const lastIdx = a0SignalList.findLastIndex((el) => el.fenxingType !== 0);
      if (Math.abs(lastIdx - a0SignalList.length) < 8) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A0",
          message:
            "出现MACD金死叉+强势顶底分型开仓/平仓判定" +
            (a1anda2DirectIsSame ? "【A1和A2级别趋势方向相同】" : ""),
          a1anda2DirectIsSame: a1anda2DirectIsSame,
        });
      }
    }
    const a1SignalList = item.a1SignalList;
    if (a1SignalList[a1SignalList.length - 1].fenxingType !== 0) {
      const lastIdx = a1SignalList.findLastIndex((el) => el.crossType !== 0);
      if (Math.abs(lastIdx - a1SignalList.length) < 8) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A1",
          message: "出现MACD金死叉+强势顶底分型开仓/平仓判定",
        });
      }
    }
    if (a1SignalList[a1SignalList.length - 1].crossType !== 0) {
      const lastIdx = a1SignalList.findLastIndex((el) => el.fenxingType !== 0);
      if (Math.abs(lastIdx - a1SignalList.length) < 8) {
        classifiedList.push({
          symbol: item.symbol,
          symbolName: symbolName,
          stage: "A1",
          message: "出现MACD金死叉+强势顶底分型开仓/平仓判定",
        });
      }
    }
  }
  return classifiedList;
};
const classifiedList = computed(() => {
  return getClassifiedTableData(tableData.value);
});
watch(classifiedList, (newList) => {
  Notification.requestPermission().then((result) => {
    if (result === "granted") {
      const arr = newList
        .filter((el) => el.a1anda2DirectIsSame)
        .map((el) => {
          const product = futuresProductList.find((item) => item.value === el.symbol);
          if (!product) return;
          return product.label;
        });
      arr.length > 0 &&
        new Notification("开平仓预警", { body: `【${arr.join("、")}】有开仓/平仓机会` });
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
      <div v-if="classifiedList.length > 0" class="warningResult">
        <div
          v-for="(item, index) in classifiedList"
          :key="index"
          :style="{ color: item.a1anda2DirectIsSame ? 'red' : '' }"
        >
          {{ item.symbolName }}({{ item.symbol }})-{{ item.stage }}级别：{{ item.message }}
        </div>
      </div>
      <div v-else class="warningResult">无</div>
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
    .warningResult {
      flex: 1;
    }
  }
}
</style>
