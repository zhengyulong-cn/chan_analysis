<script setup lang="ts">
import { IKLineData } from "@/global/klineType";
import { createChart, IChartApi, ISeriesApi } from "lightweight-charts";
import { onMounted, onUnmounted, PropType, ref, watch } from "vue";
import {
  histogramSeriesOptions,
  ICommonChartOptions,
  chartColors,
  lineSeriesOptions,
} from "./config";
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
  commonChartOptions: {
    type: Object as PropType<ICommonChartOptions>,
    required: true,
  },
  stage: {
    type: Number as PropType<20 | 80 | 320>,
    required: true,
  },
});

const chartContainer = ref();
let chart: IChartApi | null = null;
let macdSeries: ISeriesApi<"Histogram"> | null = null;
let fastLineSeries: ISeriesApi<"Line"> | null = null;
let slowLineSeries: ISeriesApi<"Line"> | null = null;
onMounted(() => {
  chart = createChart(chartContainer.value, {
    ...props.commonChartOptions,
  });
  // 红绿柱
  macdSeries = chart.addHistogramSeries(histogramSeriesOptions.value);
  macdSeries.setData(
    props.data.macd.map((el) => {
      const macdListItem = el[`macdList${props.stage}`] ?? 0;
      return {
        time: el.time,
        value: macdListItem,
        color:
          macdListItem && macdListItem > 0
            ? chartColors.value.upColor
            : chartColors.value.downColor,
      };
    })
  );
  // 白线
  fastLineSeries = chart.addLineSeries({
    ...lineSeriesOptions.value,
    color: chartColors.value.macdFastLineColor,
  });
  fastLineSeries.setData(
    props.data.macd.map((el) => {
      const macdFastLineItem = el[`macdFastLine${props.stage}`] ?? 0;
      return {
        time: el.time,
        value: macdFastLineItem,
      };
    })
  );
  // 黄线
  slowLineSeries = chart.addLineSeries({
    ...lineSeriesOptions.value,
    color: chartColors.value.macdSlowLineColor,
  });
  slowLineSeries.setData(
    props.data.macd.map((el) => {
      const macdSlowLineItem = el[`macdSlowLine${props.stage}`] ?? 0;
      return {
        time: el.time,
        value: macdSlowLineItem,
      };
    })
  );
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
  if (macdSeries) {
    macdSeries = null;
  }
  window.removeEventListener("resize", resizeHandler);
});
const fitContent = () => {
  if (!chart) return;
  chart.timeScale().fitContent();
};
defineExpose({
  getChart: () => chart,
  getMACDSeries: () => macdSeries,
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
  () => props.data.macd,
  (newData: any[]) => {
    if (!macdSeries) return;
    macdSeries.setData(
      newData.map((el) => {
        const macdListItem = el[`macdList${props.stage}`] ?? 0;
        return {
          time: el.time,
          value: macdListItem,
          color:
            macdListItem && macdListItem > 0
              ? chartColors.value.upColor
              : chartColors.value.downColor,
        };
      })
    );
    if (!fastLineSeries) return;
    fastLineSeries.setData(
      newData.map((el) => {
        const macdFastLineItem = el[`macdFastLine${props.stage}`] ?? 0;
        return {
          time: el.time,
          value: macdFastLineItem,
        };
      })
    );
    if (!slowLineSeries) return;
    slowLineSeries.setData(
      newData.map((el) => {
        const macdSlowLineItem = el[`macdSlowLine${props.stage}`] ?? 0;
        return {
          time: el.time,
          value: macdSlowLineItem,
        };
      })
    );
  }
);
</script>

<template>
  <div class="lw-chart" ref="chartContainer"></div>
</template>

<style lang="less" scoped>
.lw-chart {
  height: 10rem;
  position: relative;
}
</style>
