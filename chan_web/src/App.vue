<script setup>
import Layout from "./layouts/Layout.vue";
</script>

<template>
  <Layout>
    <template v-slot:layoutContent>
      <router-view />
    </template>
  </Layout>
</template>
<style scoped></style>
