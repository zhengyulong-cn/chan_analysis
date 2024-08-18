export enum KLineLevelEnum {
  Level_15M = 15,
  Level_60M = 60,
  Level_240M = 240,
}

export const kLineLevelList = [
  { label: "15分钟", value: KLineLevelEnum.Level_15M },
  { label: "60分钟", value: KLineLevelEnum.Level_60M },
  { label: "240分钟", value: KLineLevelEnum.Level_240M },
];

export const futuresProductList = [
  { label: "焦煤主连", value: "JM0" },
  { label: "螺纹钢主连", value: "RB0" },
  { label: "锰硅主连", value: "SM0" },
  { label: "铁矿石主连", value: "I0" },
  { label: "纯碱主连", value: "SA0" },
  { label: "尿素主连", value: "UR0" },
  { label: "沪银主连", value: "AG0" },
  { label: "PTA主连", value: "TA0" },
  { label: "纸浆主连", value: "SP0" },
  { label: "PVC主连", value: "V0" },
  { label: "棕榈油主连", value: "P0" },
  { label: "豆油主连", value: "Y0" },
  { label: "菜粕主连", value: "RM0" },
  { label: "白糖主连", value: "SR0" },
  { label: "棉花主连", value: "CF0" },
  { label: "燃油主连", value: "FU0" },
  { label: "沪镍主连", value: "NI0" },
];
