export interface ISignalListItem {
  datetime: string;
  crossType: number;
  fenxingType: number;
}

export interface IFuturesMonitorTableItem {
  symbol: string;
  a0Direct: number;
  a1Direct: number;
  a2Direct: number;
  a0SignalList: Array<ISignalListItem>;
  a1SignalList: Array<ISignalListItem>;
}

export type IFuturesMonitorTable = Array<IFuturesMonitorTableItem>;
