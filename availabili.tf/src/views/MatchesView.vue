<script setup lang="ts">
import AddMatchDialog from "@/components/AddMatchDialog.vue";
import { useMatchesStore } from "@/stores/matches";
import { onMounted } from "vue";

const matchesStore = useMatchesStore();

onMounted(() => {
  matchesStore.fetchMatches();
});
</script>

<template>
  <main>
    <div class="header">
      <h1>
        <i class="bi bi-trophy-fill margin"></i>
        Matches you've played
      </h1>
      <div class="button-group">
        <AddMatchDialog />
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>RED</th>
          <th>BLU</th>
          <th>Match Date</th>
          <th>logs.tf URL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="match in matchesStore.matches" :key="match.logsTfId">
          <td>{{ match.redScore }}</td>
          <td>{{ match.blueScore }}</td>
          <td>{{ match.matchTime }}</td>
          <td>
            <a :href="`https://logs.tf/${match.logsTfId}`" target="_blank">
              #{{ match.logsTfId }}
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.5rem;
}

table {
  width: 100%;
}

th {
  text-align: left;
  font-weight: 800;
}
</style>
