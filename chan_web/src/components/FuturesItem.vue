<script lang="ts" setup>
import { onMounted, reactive, watch } from "vue";
import { KLineLevelEnum, kLineLevelList, futuresProductList } from "@/global/constants/futures";
import { getFuturesListApi } from "@/api/modules";
import KLineChart from "./charts/KLineChart.vue";
import { IKLineData } from "@/global/klineType";
import dayjs from "dayjs";
import _ from "lodash";
import { useDark } from "@vueuse/core";
const isDark = useDark();

interface ISettings {
  symbol: string;
  period: KLineLevelEnum;
}
const settings: ISettings = reactive({
  symbol: futuresProductList[0].value,
  period: kLineLevelList[0].value,
});
const kLineData: IKLineData = reactive({
  kLineList: [],
  kLineListCount: 0,
  period: KLineLevelEnum.Level_15M,
  symbol: settings.symbol,
  chanCentral: {},
  chanPens: {},
  headers: [],
});
const kLineChartOptions = reactive({
  layoutOptions: { background: { color: "#222" }, textColor: "#C3BCDB" },
  gridOptions: {
    vertLines: { color: "#444" },
    horzLines: { color: "#444" },
  },
  priceScaleOptions: { borderVisible: false },
  timeScaleOptions: { timeVisible: true, borderVisible: false },
  candlestickSeriesOptions: {
    upColor: "#ef5350",
    downColor: "#26a69a",
    borderVisible: false,
    wickUpColor: "#ef5350",
    wickDownColor: "#26a69a",
  },
});

// 组件挂载时加载数据
onMounted(() => {
  loadData(futuresProductList[0].value, kLineLevelList[0].value);
});

const loadData = (symbol: string, period: KLineLevelEnum) => {
  getFuturesListApi({
    symbol: symbol,
    period: period,
  }).then((res) => {
    const data = res.data as any;
    if (!_.isArray(data?.kLineList)) {
      return;
    }
    kLineData.kLineList = data.kLineList.map((el: any) => {
      return {
        close: el.close,
        high: el.high,
        low: el.low,
        open: el.open,
        time: dayjs(el.datetime).unix(),
        MA5: el.MA5,
        MA10: el.MA10,
        MA20: el.MA20,
        MA40: el.MA40,
        MA80: el.MA80,
        MA160: el.MA160,
        MA320: el.MA320,
      };
    });
  });
};

watch(
  () => settings,
  (newValue) => {
    if (newValue.symbol && newValue.period) {
      loadData(newValue.symbol, newValue.period);
    }
  },
  { deep: true }
);

watch(isDark, (newValue) => {
  if (newValue) {
    kLineChartOptions.layoutOptions = {
      background: { color: "#222" },
      textColor: "#C3BCDB",
    };
    kLineChartOptions.gridOptions = {
      vertLines: { color: "#444" },
      horzLines: { color: "#444" },
    };
  } else {
    kLineChartOptions.layoutOptions = {
      background: { color: "#fff" },
      textColor: "#000000",
    };
    kLineChartOptions.gridOptions = {
      vertLines: { color: "#dcdfe6" },
      horzLines: { color: "#dcdfe6" },
    };
  }
});
</script>

<template>
  <div class="futuresItem">
    <div class="settings">
      <el-select class="selectItem" placeholder="请选择期货品种" v-model="settings.symbol">
        <el-option
          v-for="product in futuresProductList"
          :key="product.value"
          :label="product.label"
          :value="product.value"
        ></el-option>
      </el-select>
      <el-select class="selectItem" placeholder="请选择周期" v-model="settings.period">
        <el-option
          v-for="period in kLineLevelList"
          :key="period.value"
          :label="period.label"
          :value="period.value"
        ></el-option>
      </el-select>
    </div>
    <div class="chartContainer">
      <KLineChart
        autosize
        :data="kLineData.kLineList"
        :time-scale-options="kLineChartOptions.timeScaleOptions"
        :price-scale-options="kLineChartOptions.priceScaleOptions"
        :layout-options="kLineChartOptions.layoutOptions"
        :grid-options="kLineChartOptions.gridOptions"
        :candlestick-series-options="kLineChartOptions.candlestickSeriesOptions"
      />
    </div>
  </div>
</template>

<style lang="less" scoped>
.futuresItem {
  .settings {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;

    .selectItem {
      width: 10rem;
    }
  }

  .chartContainer {
    height: 30rem;
  }
}
</style>
