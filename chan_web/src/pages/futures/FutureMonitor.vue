<script lang="ts" setup>
import { getFuturesListWarningApi } from "@/api/modules";
import FuturesMonitorTable from "@/components/FuturesMonitorTable.vue";
import FuturesWarning from "@/components/FuturesWarning.vue";
import { futuresProductList } from "@/global/constants/futures";
import { IFuturesMonitorTable } from "@/global/monitorType";
import { ref, onMounted } from "vue";
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
</script>

<template>
  <div class="pageBox">
    <header class="headerMenu">
      <div>最后更新时间：{{ lastUpdatedAt ?? "无记录" }}</div>
      <el-icon class="refresh" size="24" @click="handleUpdateClick"><Refresh /></el-icon>
    </header>
    <section class="bodySection">
      <div class="futuresMonitorTable">
        <FuturesMonitorTable :table-data="tableData" :loading="isLoading" />
      </div>
      <div class="futuresWarning">
        <FuturesWarning :table-data="tableData" :loading="isLoading" />
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
      flex: 1;
      width: 50%;
      height: 100%;
    }
    .futuresWarning {
      flex: 1;
    }
  }
}
</style>
