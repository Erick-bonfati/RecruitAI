<template>
  <div class="page">

    <HeaderBar />

    <main class="shell main">
      <RouterView />
    </main>

    <FooterBar />
  </div>
</template>

<script setup>
import HeaderBar from './components/HeaderBar.vue'
import FooterBar from './components/FooterBar.vue'
</script>
