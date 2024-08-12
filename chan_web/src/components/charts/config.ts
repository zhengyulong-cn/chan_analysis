import { useDark } from "@vueuse/core";
import dayjs from "dayjs";
import { LineWidth } from "lightweight-charts";
import _ from "lodash";
import { computed } from "vue";
const isDark = useDark();

export const chartColors = computed(() => {
  if (isDark.value) {
    return {
      backgroudColor: "#222",
      textColor: "#C3BCDB",
      vhLinesColor: "#444",
      upColor: "#ef5350",
      downColor: "#26a69a",
      macdFastLineColor: "#FFFFFF",
      macdSlowLineColor: "#e6a23c",
    };
  }
  return {
    backgroudColor: "#FFFFFF",
    textColor: "#000000",
    vhLinesColor: "#dcdfe6",
    upColor: "#ef5350",
    downColor: "#26a69a",
    macdFastLineColor: "#000000",
    macdSlowLineColor: "#e6a23c",
  };
});

export interface ICommonChartOptions {
  layout: Record<string, any>;
  grid: Record<string, any>;
  rightPriceScale: Record<string, any>;
  timeScale: Record<string, any>;
  crosshair: Record<string, any>;
  localization: Record<string, any>;
}

export const commonChartOptions = computed<ICommonChartOptions>(() => {
  return {
    layout: {
      background: { color: chartColors.value.backgroudColor },
      textColor: chartColors.value.textColor,
    },
    grid: {
      vertLines: { color: chartColors.value.vhLinesColor },
      horzLines: { color: chartColors.value.vhLinesColor },
    },
    rightPriceScale: { borderVisible: false },
    timeScale: { timeVisible: true, borderVisible: false },
    crosshair: {
      mode: 0,
    },
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
  };
});

export const lineSeriesOptions = computed(() => {
  return {
    color: chartColors.value.textColor,
    lineWidth: 2 as LineWidth,
    priceLineVisible: true,
  };
});

export const candlestickSeriesOptions = computed(() => {
  return {
    upColor: chartColors.value.upColor,
    downColor: chartColors.value.downColor,
    borderVisible: false,
    wickUpColor: chartColors.value.upColor,
    wickDownColor: chartColors.value.downColor,
  };
});

export const histogramSeriesOptions = computed(() => {
  return {
    color: chartColors.value.downColor,
  };
});
