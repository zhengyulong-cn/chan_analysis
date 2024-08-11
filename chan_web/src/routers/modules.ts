import { RouteRecordRaw } from "vue-router";

export const RouterModules: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/futures",
  },
  {
    path: "/home",
    name: "Home",
    component: () => import("@/pages/Home.vue"),
    meta: {
      icon: "HomeFilled",
      title: "首页",
    },
  },
  {
    path: "/futures",
    name: "Futures",
    meta: {
      icon: "TrendCharts",
      title: "期货",
    },
    children: [
      {
        path: "/futures/huishang",
        component: () => import("@/pages/Huishang.vue"),
        meta: {
          icon: "",
          title: "徽商期货保证金",
        },
      },
      {
        path: "/futures/detail",
        component: () => import("@/pages/Futures.vue"),
        meta: {
          icon: "",
          title: "期货单品详情",
        },
      },
    ],
  },
];
