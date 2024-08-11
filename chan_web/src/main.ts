import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'
// ElementPlus组件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// ElementPlus图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// ElementPlus暗黑模式颜色
import 'element-plus/theme-chalk/dark/css-vars.css'
// 全局颜色
import './global.less'
// 初始化样式
import './style.css'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
// 引入图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.mount('#app')
