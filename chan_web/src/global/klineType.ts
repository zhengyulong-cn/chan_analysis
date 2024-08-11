import { KLineLevelEnum } from "./constants/futures";

export interface IKLine {
  high: number;
  low: number;
  open: number;
  close: number;
  time: string | number;
  MA5: number;
  MA10: number;
  MA20: number;
  MA40: number;
  MA80: number;
  MA160: number;
  MA320: number;
}

export interface IKLineData {
  symbol: string;
  period: KLineLevelEnum;
  headers: Array<string>;
  kLineListCount: number;
  kLineList: Array<IKLine>;
  chanPens: Record<string, any>;
  chanCentral: Record<string, any>;
}
