<script lang="ts" setup>
import { onMounted, onUnmounted, reactive, watch } from "vue";
import { KLineLevelEnum, kLineLevelList, futuresProductList } from "@/global/constants/futures";
import { getFuturesListApi } from "@/api/modules";
import { IKLineData } from "@/global/klineType";
import dayjs from "dayjs";
import _ from "lodash";
import KLineCentre from "./charts/KLineCentre.vue";

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
  chanCentral: {
    a0CentralList: [],
    a1CentralList: [],
  },
  chanPens: {
    a0PenPointList: [],
    a1PenPointList: [],
    a2PenPointList: [],
  },
  headers: [],
  macd: [],
});

// 组件挂载时加载数据
onMounted(() => {
  loadData(futuresProductList[0].value, kLineLevelList[0].value);
});
/**
 * 加载图表数据
 * @param symbol 品种
 * @param period 级别，15min、60min、240min
 */
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
    kLineData.macd = data.macd.map((el: any) => {
      return {
        ...el,
        time: dayjs(el.datetime).unix(),
      };
    });
    kLineData.chanPens = {
      a0PenPointList: data.chanPens["a0PenPointList"].map((el) => {
        return {
          time: dayjs(el.datetime).unix(),
          value: el.price,
        };
      }),
      a1PenPointList: data.chanPens["a1PenPointList"].map((el) => {
        return {
          time: dayjs(el.datetime).unix(),
          value: el.price,
        };
      }),
      a2PenPointList: data.chanPens["a2PenPointList"].map((el) => {
        return {
          time: dayjs(el.datetime).unix(),
          value: el.price,
        };
      }),
    };
    kLineData.chanCentral = {
      a0CentralList: data.chanCentral["a0CentralList"],
      a1CentralList: data.chanCentral["a1CentralList"],
    };
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
      <KLineCentre :data="kLineData" autosize />
    </div>
  </div>
</template>

<style lang="less" scoped>
.futuresItem {
  display: flex;
  flex-direction: column;
  .settings {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;

    .selectItem {
      width: 10rem;
    }
  }

  .chartContainer {
    flex: 1;
  }
}
</style>
