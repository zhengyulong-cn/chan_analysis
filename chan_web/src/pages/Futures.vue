<script lang="ts" setup>
import FuturesItem from "@/components/FuturesItem.vue";
</script>

<template>
  <div class="pageBox">
    <FuturesItem />
  </div>
</template>

<style lang="less" scoped>
.pageBox {
  background-color: var(--el-bg-color);
  overflow: auto;
  border-radius: 1rem;
  padding: 1rem;
  max-height: calc(100% - 2rem);
  height: 100%;
}
</style>
