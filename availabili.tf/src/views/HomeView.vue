<script setup lang="ts">
import GithubCommitHistory from "@/components/GithubCommitHistory.vue";
import TeamsListSidebar from "../components/TeamsListSidebar.vue";
</script>

<template>
  <main>
    <div class="home-view-container">
      <div class="left">
        <TeamsListSidebar />
      </div>
      <div class="right">
        <GithubCommitHistory />
      </div>
    </div>
  </main>
</template>

<style scoped>
.home-view-container {
  display: flex;
  gap: 2rem;
}

.left {
  flex: 2;
}

.right {
  flex: 1;
}

@media (max-width: 1024px) {
  .home-view-container {
    flex-direction: column;
  }
}
</style>
