import axios from '@/api/axios'
import { KLineLevelEnum } from "@/global/constants/futures"
import { IKLineData } from '@/global/klineType'

export const getFuturesListApi = (params: { symbol: string, period: KLineLevelEnum }) => {
  return axios.get('/future_data', params)
}