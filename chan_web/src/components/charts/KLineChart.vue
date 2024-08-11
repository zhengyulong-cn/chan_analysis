<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import { createChart, IChartApi, ISeriesApi } from "lightweight-charts";
import dayjs from "dayjs";
import _ from "lodash";
import { IKLine } from "@/global/klineType";

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  autosize: {
    default: true,
    type: Boolean,
  },
  layoutOptions: {
    type: Object,
  },
  gridOptions: {
    type: Object,
  },
  candlestickSeriesOptions: {
    type: Object,
    required: true,
  },
  priceScaleOptions: {
    type: Object,
  },
  timeScaleOptions: {
    type: Object,
  },
});

let kSeries: ISeriesApi<"Candlestick"> | null = null;
let ma5Series: ISeriesApi<"Line"> | null = null;
let ma10Series: ISeriesApi<"Line"> | null = null;
let ma20Series: ISeriesApi<"Line"> | null = null;
let ma40Series: ISeriesApi<"Line"> | null = null;
let ma80Series: ISeriesApi<"Line"> | null = null;
let ma160Series: ISeriesApi<"Line"> | null = null;
let ma320Series: ISeriesApi<"Line"> | null = null;
let chart: IChartApi | null = null;

const chartContainer = ref();

const fitContent = () => {
  if (!chart) return;
  chart.timeScale().fitContent();
};

const getChart = () => {
  return chart;
};

defineExpose({ fitContent, getChart });

const resizeHandler = () => {
  if (!chart || !chartContainer.value) return;
  const dimensions = chartContainer.value.getBoundingClientRect();
  chart.resize(dimensions.width, dimensions.height);
};

const addSeriesAndData = (props) => {
  if (!chart) return;
  chart.applyOptions({
    localization: {
      locale: "zh-CN",
      timeFormatter: (time: number | string) => {
        if (_.isNumber(time)) {
          return dayjs(time * 1000).format("YYYY年MM月DD日 HH:mm");
        } else {
          return time;
        }
      },
    },
    crosshair: {
      mode: 0,
    },
    layout: props.layoutOptions,
    grid: props.gridOptions,
    timeScale: props.timeScaleOptions,
    rightPriceScale: props.priceScaleOptions,
  });
  ma5Series = chart.addLineSeries({ color: "#FFFFFF", lineWidth: 1, priceLineVisible: false });
  ma10Series = chart.addLineSeries({ color: "#ffff00", lineWidth: 1, priceLineVisible: false });
  ma20Series = chart.addLineSeries({ color: "#8000ff", lineWidth: 1, priceLineVisible: false });
  ma40Series = chart.addLineSeries({ color: "#00ff00", lineWidth: 1, priceLineVisible: false });
  ma80Series = chart.addLineSeries({ color: "#0080ff", lineWidth: 1, priceLineVisible: false });
  ma160Series = chart.addLineSeries({ color: "#ff7f00", lineWidth: 1, priceLineVisible: false });
  ma320Series = chart.addLineSeries({ color: "#ff0080", lineWidth: 1, priceLineVisible: false });
  kSeries = chart.addCandlestickSeries(props.candlestickSeriesOptions);
  ma5Series.setData(
    props.data.map((el) => ({ time: el.time, value: el.MA5 })).filter((el) => el.value)
  );
  kSeries.setData(props.data);
};

onMounted(() => {
  chart = createChart(chartContainer.value);
  addSeriesAndData(props);

  // 添加十字光标的Tooltip
  const toolTip = document.createElement("div");
  toolTip.style.position = "absolute";
  toolTip.style.zIndex = "1000";
  toolTip.style.top = "0";
  toolTip.style.left = "0";
  chartContainer.value.appendChild(toolTip);
  chart.subscribeCrosshairMove((param) => {
    if (
      param.point === undefined ||
      !param.time ||
      param.point.x < 0 ||
      param.point.x > chartContainer.value.clientWidth ||
      param.point.y < 0 ||
      param.point.y > chartContainer.value.clientHeight
    ) {
      toolTip.style.display = "none";
    } else {
      toolTip.style.display = "block";
      const data = param.seriesData.get(kSeries!) as IKLine;
      const open = data.open;
      const close = data.close;
      const high = data.high;
      const low = data.low;
      // const MA5 = param.seriesData.get(ma5Series!)?.value;
      // const MA10 = param.seriesData.get(ma10Series!)?.value;
      // const MA20 = param.seriesData.get(ma20Series!)?.value;
      // const MA40 = param.seriesData.get(ma40Series!)?.value;
      // const MA80 = param.seriesData.get(ma80Series!)?.value;
      // const MA160 = param.seriesData.get(ma160Series!)?.value;
      // const MA320 = param.seriesData.get(ma320Series!)?.value;

      let time = data.time;
      if (_.isNumber(time)) {
        time = dayjs(time * 1000).format("MM/DD HH:mm");
      }
      const color =
        open <= close
          ? props.candlestickSeriesOptions.upColor
          : props.candlestickSeriesOptions.downColor;
      toolTip.innerHTML = `
        <div>${time}</div>
        <div>
          <span>开盘</span>
          <span style="color: ${color}">${open}</span>
        </div>
        <div>
          <span>收盘</span>
          <span style="color: ${color}">${close}</span>
        </div>
        <div>
          <span>最高</span>
          <span style="color: ${color}">${high}</span>
        </div>
        <div>
          <span>最低</span>
          <span style="color: ${color}">${low}</span>
        </div>
      `;
    }
  });

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
  () => props.data,
  (newData: any[]) => {
    if (!kSeries) return;
    kSeries.setData(newData);
    if (!ma5Series) return;
    ma5Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA5 })).filter((el) => el.value)
    );
    if (!ma10Series) return;
    ma10Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA10 })).filter((el) => el.value)
    );
    if (!ma20Series) return;
    ma20Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA20 })).filter((el) => el.value)
    );
    if (!ma40Series) return;
    ma40Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA40 })).filter((el) => el.value)
    );
    if (!ma80Series) return;
    ma80Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA80 })).filter((el) => el.value)
    );
    if (!ma160Series) return;
    ma160Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA160 })).filter((el) => el.value)
    );
    if (!ma320Series) return;
    ma320Series.setData(
      newData.map((el) => ({ time: el.time, value: el.MA320 })).filter((el) => el.value)
    );
  }
);

watch(
  () => props.layoutOptions,
  (newOptions) => {
    if (!chart) return;
    chart.applyOptions({
      layout: newOptions,
    });
  }
);
watch(
  () => props.gridOptions,
  (newOptions) => {
    if (!chart) return;
    chart.applyOptions({
      grid: newOptions,
    });
  }
);
</script>

<template>
  <div class="lw-chart" ref="chartContainer"></div>
</template>

<style scoped>
.lw-chart {
  height: 100%;
  position: relative;
}
</style>
