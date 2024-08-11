<script lang="ts" setup></script>

<template>
  <div class="pageBox">
    <span v-for="i in 1000">主要功能{{ i }}</span>
  </div>
</template>

<style lang="less" scoped>
.pageBox {
  background-color: var(--el-bg-color);
  height: 100%;
  overflow: auto;
  border-radius: 0.5rem;
}
</style>
