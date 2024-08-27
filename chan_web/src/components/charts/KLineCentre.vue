<script setup lang="ts">
import { IKLineData } from "@/global/klineType";
import { onMounted, PropType, ref } from "vue";
import { commonChartOptions } from "./config";
import KLineChart from "./KLineChart.vue";
import MACDChart from "./MACDChart.vue";
import { IChartApi, ISeriesApi } from "lightweight-charts";
import _ from "lodash";

const props = defineProps({
  data: {
    type: Object as PropType<IKLineData>,
    required: true,
  },
  autosize: {
    default: true,
    type: Boolean,
  },
});
const kLineChartRef = ref<{
  getChart: () => IChartApi;
  getKSeries: () => ISeriesApi<"Candlestick">;
} | null>(null);
const macdChart20Ref = ref<{
  getChart: () => IChartApi;
  getMACDSeries: () => ISeriesApi<"Histogram">;
} | null>(null);
const macdChart80Ref = ref<{
  getChart: () => IChartApi;
  getMACDSeries: () => ISeriesApi<"Histogram">;
} | null>(null);
onMounted(() => {
  // if (kLineChartRef.value && macdChart20Ref.value) {
  //   const kLineChart = kLineChartRef.value.getChart();
  //   const macdChart20 = macdChart20Ref.value.getChart();
  //   const kSeries = kLineChartRef.value.getKSeries();
  //   const macdSeries = macdChart20Ref.value.getMACDSeries();
  //   kLineChart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
  //     range && macdChart20.timeScale().setVisibleLogicalRange(range);
  //   });
  //   macdChart20.timeScale().subscribeVisibleLogicalRangeChange((range) => {
  //     range && kLineChart.timeScale().setVisibleLogicalRange(range);
  //   });
  //   kLineChart.subscribeCrosshairMove((params) => {
  //     const dataPoint = getCrosshairDataPoint(kSeries, params);
  //     syncCrosshair(macdChart20, macdSeries, dataPoint?.time, 0.01);
  //   });
  //   macdChart20.subscribeCrosshairMove((params) => {
  //     const dataPoint = getCrosshairDataPoint(macdSeries, params);
  //     syncCrosshair(kLineChart, kSeries, dataPoint?.time, 1400.0);
  //   });
  // }
});

const getCrosshairDataPoint = (series, param) => {
  if (!param.time) {
    return null;
  }
  const dataPoint = param.seriesData.get(series);
  return dataPoint || null;
};
const syncCrosshair = (chart, series, time, price) => {
  if (!chart || !series) {
    return;
  }
  if (!_.isNil(time) && !_.isNil(price)) {
    chart.setCrosshairPosition(price, time, series);
    return;
  }
  chart.clearCrosshairPosition();
};
</script>

<template>
  <div class="klineCentre">
    <KLineChart
      ref="kLineChartRef"
      :data="props.data"
      autosize
      :common-chart-options="commonChartOptions"
    />
    <!-- <MACDChart
      ref="macdChart20Ref"
      :data="props.data"
      autosize
      :common-chart-options="commonChartOptions"
      :stage="20"
    />
    <MACDChart
      ref="macdChart80Ref"
      :data="props.data"
      autosize
      :common-chart-options="commonChartOptions"
      :stage="80"
    /> -->
  </div>
</template>

<style lang="less" scoped></style>
