<script lang="ts" setup>
import { IFuturesMonitorTable } from "@/global/monitorType";
import { PropType } from "vue";
import { futuresProductList } from "@/global/constants/futures";
const props = defineProps({
  tableData: {
    type: Array as PropType<IFuturesMonitorTable>,
    required: true,
  },
  loading: {
    type: Boolean,
  },
});
const formatSymbolText = (symbol: string) => {
  const product = futuresProductList.find((el) => el.value === symbol);
  if (!product) return "";
  return `${product.label}-${product.value}`;
};
</script>

<template>
  <el-table
    :data="props.tableData"
    style="width: 100%"
    class="futuresMonitorTable"
    v-loading="props.loading"
  >
    <el-table-column prop="symbol" label="合约" fixed="left">
      <template #default="scope">
        <div>{{ formatSymbolText(scope.row.symbol) }}</div>
      </template>
    </el-table-column>
    <el-table-column label="趋势方向" width="90">
      <template #default="scope">
        <div>A0: {{ scope.row.a0Direct === 1 ? "上涨" : "下跌" }}</div>
        <div>A1: {{ scope.row.a1Direct === 1 ? "上涨" : "下跌" }}</div>
        <div>A2: {{ scope.row.a2Direct === 1 ? "上涨" : "下跌" }}</div>
      </template>
    </el-table-column>
    <el-table-column prop="a0SignalList" label="A0信号" width="300">
      <template #default="scope">
        <div v-for="item in scope.row.a0SignalList" :key="item.datetime" class="signalListBox">
          <span>{{ item.datetime }}</span>
          <span>{{ item.crossType === 1 ? "金叉" : item.crossType === -1 ? "死叉" : "-" }}</span>
          <span>{{
            item.fenxingType === 1 ? "强势底分型" : item.fenxingType === -1 ? "强势顶分型" : "-"
          }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="a1SignalList" label="A1信号" width="300">
      <template #default="scope">
        <div v-for="item in scope.row.a1SignalList" :key="item.datetime" class="signalListBox">
          <span>{{ item.datetime }}</span>
          <span>{{ item.crossType === 1 ? "金叉" : item.crossType === -1 ? "死叉" : "-" }}</span>
          <span>{{
            item.fenxingType === 1 ? "强势底分型" : item.fenxingType === -1 ? "强势顶分型" : "-"
          }}</span>
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<style lang="less" scoped>
.futuresMonitorTable {
  flex: 1;
}
.signalListBox {
  display: flex;
  flex-direction: row;
  column-gap: 0.5rem;
  .highlightMark {
    color: red;
  }
}
</style>
