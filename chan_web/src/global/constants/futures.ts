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
  { label: "铁矿石主连", value: "I0" },
  { label: "沪镍主连", value: "NI0" },
  { label: "螺纹钢主连", value: "RB0" },
  { label: "纯碱主连", value: "SA0" },
  { label: "白银主连", value: "AG0" },
  { label: "豆油主连", value: "Y0" },
];
