import { KLineLevelEnum } from "./constants/futures";
import { Time } from "lightweight-charts";

export interface IKLine {
  high: number;
  low: number;
  open: number;
  close: number;
  time: Time;
  MA5: number | null;
  MA10: number | null;
  MA20: number | null;
  MA40: number | null;
  MA80: number | null;
  MA160: number | null;
  MA320: number | null;
}

export interface IKLineItem {
  time: Time;
  macdFastLine20: number | null;
  macdFastLine80: number | null;
  macdFastLine320: number | null;
  macdList20: number | null;
  macdList80: number | null;
  macdList320: number | null;
  macdSlowLine20: number | null;
  macdSlowLine80: number | null;
  macdSlowLine320: number | null;
}

export interface IKLineData {
  symbol: string;
  period: KLineLevelEnum;
  headers: Array<string>;
  kLineListCount: number;
  kLineList: Array<IKLine>;
  chanPens: Record<"a0PenPointList" | "a1PenPointList" | "a2PenPointList", any[]>;
  chanCentral: Record<"a0CentralList" | "a1CentralList", any>;
  macd: Array<IKLineItem>;
}
