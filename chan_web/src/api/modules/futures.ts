import axios from "@/api/axios";
import { KLineLevelEnum } from "@/global/constants/futures";

export const getFutureDataApi = (params: { symbol: string; period: KLineLevelEnum }) => {
  return axios.get("/future_data", params);
};

export const getFuturesListWarningApi = (symbolList: Array<string>) => {
  return axios.post("/futures_list_warning", {
    symbol_list: symbolList,
  });
};
