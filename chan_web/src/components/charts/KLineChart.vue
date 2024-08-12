<script setup lang="ts">
import { IKLineData } from "@/global/klineType";
import { createChart, IChartApi, ISeriesApi } from "lightweight-charts";
import { onMounted, onUnmounted, PropType, ref, watch } from "vue";
import { candlestickSeriesOptions, ICommonChartOptions, lineSeriesOptions } from "./config";

const props = defineProps({
  data: {
    type: Object as PropType<IKLineData>,
    required: true,
  },
  autosize: {
    default: true,
    type: Boolean,
  },
  commonChartOptions: {
    type: Object as PropType<ICommonChartOptions>,
    required: true,
  },
});

const chartContainer = ref();
let chart: IChartApi | null = null;
let kSeries: ISeriesApi<"Candlestick"> | null = null;
let chanPenA0Series: ISeriesApi<"Line"> | null = null;
let chanPenA1Series: ISeriesApi<"Line"> | null = null;
let chanPenA2Series: ISeriesApi<"Line"> | null = null;
onMounted(() => {
  chart = createChart(chartContainer.value, {
    ...props.commonChartOptions,
  });
  // 隐藏K线图的时间刻度
  // chart.applyOptions({
  //   timeScale: {
  //     visible: false,
  //   },
  // });
  // 绘制基本K线
  kSeries = chart.addCandlestickSeries(candlestickSeriesOptions.value);
  kSeries.setData(props.data.kLineList);
  // 绘制笔
  chanPenA0Series = chart.addLineSeries({
    ...lineSeriesOptions.value,
    color: "yellow",
  });
  chanPenA0Series.setData(props.data.chanPens["a0PenPointList"]);
  chanPenA1Series = chart.addLineSeries({
    ...lineSeriesOptions.value,
    color: "cyan",
  });
  chanPenA1Series.setData(props.data.chanPens["a1PenPointList"]);
  chanPenA2Series = chart.addLineSeries({
    ...lineSeriesOptions.value,
    color: "red",
  });
  chanPenA2Series.setData(props.data.chanPens["a2PenPointList"]);
  // 时间刻度自适应
  chart.timeScale().fitContent();
  if (props.autosize) {
    window.addEventListener("resize", resizeHandler);
  }
});
onUnmounted(() => {
  if (chart) {
    chart.remove();
    chart = null;
  }
  if (kSeries) {
    kSeries = null;
  }
  window.removeEventListener("resize", resizeHandler);
});
const fitContent = () => {
  if (!chart) return;
  chart.timeScale().fitContent();
};
defineExpose({
  getChart: () => chart,
  getKSeries: () => kSeries,
});
const resizeHandler = () => {
  if (!chart || !chartContainer.value) return;
  const dimensions = chartContainer.value.getBoundingClientRect();
  chart.resize(dimensions.width, dimensions.height);
};
watch(
  () => props.autosize,
  (enabled) => {
    if (!enabled) {
      window.removeEventListener("resize", resizeHandler);
      return;
    }
    window.addEventListener("resize", resizeHandler);
  }
);
watch(
  () => props.commonChartOptions,
  (newOptions) => {
    if (!chart) return;
    chart.applyOptions(newOptions);
  }
);
watch(
  () => props.data.kLineList,
  (newData: any[]) => {
    if (!kSeries) return;
    kSeries.setData(newData);
  }
);
watch(
  () => props.data.chanPens.a0PenPointList,
  (newData: any[]) => {
    if (!chanPenA0Series) return;
    chanPenA0Series.setData(newData);
  }
);
watch(
  () => props.data.chanPens.a1PenPointList,
  (newData: any[]) => {
    if (!chanPenA1Series) return;
    chanPenA1Series.setData(newData);
  }
);
watch(
  () => props.data.chanPens.a2PenPointList,
  (newData: any[]) => {
    if (!chanPenA2Series) return;
    chanPenA2Series.setData(newData);
  }
);
</script>

<template>
  <div class="lw-chart" ref="chartContainer"></div>
</template>

<style lang="less" scoped>
.lw-chart {
  height: 30rem;
  position: relative;
}
</style>
