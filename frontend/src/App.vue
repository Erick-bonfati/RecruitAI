<template>
  <div class="page">
    <div class="ambient">
      <span class="orb orb--one"></span>
      <span class="orb orb--two"></span>
      <span class="orb orb--three"></span>
    </div>

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
