import {
  DataChangedScope,
  IChartApi,
  ISeriesApi,
  ISeriesPrimitive,
  SeriesAttachedParameter,
  SeriesOptionsMap,
  Time,
} from "lightweight-charts";
import { ensureDefined } from "./assertions";

export abstract class PluginBase implements ISeriesPrimitive<Time> {
  private _chart: IChartApi | undefined = undefined;
  private _series: ISeriesApi<keyof SeriesOptionsMap> | undefined = undefined;

  protected dataUpdated?(scope: DataChangedScope): void;
  protected requestUpdate(): void {
    if (this._requestUpdate) this._requestUpdate();
  }
  private _requestUpdate?: () => void;

  public attached({ chart, series, requestUpdate }: SeriesAttachedParameter<Time>) {
    this._chart = chart;
    this._series = series;
    this._series.subscribeDataChanged(this._fireDataUpdated);
    this._requestUpdate = requestUpdate;
    this.requestUpdate();
  }

  public detached() {
    this._series?.unsubscribeDataChanged(this._fireDataUpdated);
    this._chart = undefined;
    this._series = undefined;
    this._requestUpdate = undefined;
  }

  public get chart(): IChartApi {
    return ensureDefined(this._chart);
  }

  public get series(): ISeriesApi<keyof SeriesOptionsMap> {
    return ensureDefined(this._series);
  }

  /**
   * 此方法是一个类属性，用于维护词法this范围（由于使用了箭头函数）并确保其引用保持不变，以便我们以后可以取消订阅。
   */
  private _fireDataUpdated = (scope: DataChangedScope) => {
    if (this.dataUpdated) {
      this.dataUpdated(scope);
    }
  };
}
