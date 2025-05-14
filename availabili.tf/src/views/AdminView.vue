<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <main class="sidebar-container admin-panel">
    <nav class="sidebar">
      <div class="categories">
        <h3>Admin Panel</h3>
        <RouterLink class="tab" :to="{ name: 'admin/' }">
          General
        </RouterLink>
        <RouterLink class="tab" :to="{ name: 'admin/doas' }">
          Become User
        </RouterLink>
      </div>
    </nav>
    <div class="view">
      <RouterView />
    </div>
  </main>
</template>
