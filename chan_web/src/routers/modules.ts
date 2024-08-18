import { RouteRecordRaw } from "vue-router";

export const RouterModules: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/futures/monitor",
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
        path: "/futures/monitor",
        component: () => import("@/pages/futures/FutureMonitor.vue"),
        meta: {
          icon: "",
          title: "期货行情监控",
        },
      },
      {
        path: "/futures/detail",
        component: () => import("@/pages/futures/FutureDetail.vue"),
        meta: {
          icon: "",
          title: "期货单品详情",
        },
      },
      {
        path: "/futures/huishang",
        component: () => import("@/pages/futures/Huishang.vue"),
        meta: {
          icon: "",
          title: "徽商期货保证金",
        },
      },
    ],
  },
];
