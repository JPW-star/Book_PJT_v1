<script setup>
import { RouterView } from 'vue-router'
import AppNavbar from '@/components/common/AppNavbar.vue'
</script>

<template>
  <header>
    <AppNavbar />
  </header>

  <RouterView />
</template>

<style scoped></style>
