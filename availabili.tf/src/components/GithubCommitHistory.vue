<script setup lang="ts">
import { useCommitsStore } from "@/stores/commits";
import { onMounted, ref } from "vue";
import GithubCommitHistoryItem from "./GithubCommitHistoryItem.vue";

const commitsStore = useCommitsStore();

onMounted(() => {
  commitsStore.fetchCommits();
});
</script>

<template>
  <div class="commit-history">
    <div class="header">
      <h2>Commit History</h2>
      <a
        class="icon"
        href="https://github.com/HumanoidSandvichDispenser/availabili.tf/commits"
      >
        <button class="icon">
          <i class="bi bi-view-list"></i>
        </button>
      </a>
    </div>
    <div>
      <GithubCommitHistoryItem
        v-for="commit in commitsStore.commits.slice(0, 5)"
        :commit="commit"
      />
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
}
</style>
