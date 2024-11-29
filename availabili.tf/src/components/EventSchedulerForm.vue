<script setup lang="ts">
import { useRosterStore } from "@/stores/roster";
import moment from "moment";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const rosterStore = useRosterStore();

function saveRoster() {
  rosterStore.saveRoster(Number(route.params.teamId))
    .then(() => {
      router.push({
        name: "team-details",
        params: {
          id: route.params.teamId
        }
      });
    });
}
</script>

<template>
  <div class="event-scheduler-container">
    <h1 class="roster-title">
      Roster for Snus Brotherhood
    </h1>
    <div v-if="rosterStore.startTime">
      <span class="aside date">
        {{ moment.unix(rosterStore.startTime).format("LL LT") }}
      </span>
    </div>
    <div class="form-group margin">
      <h3>Event Name</h3>
      <input v-model="rosterStore.title" />
    </div>
    <div class="form-group margin">
      <h3>Description (optional)</h3>
      <input v-model="rosterStore.description" />
    </div>
    <div class="form-group margin">
      <div class="action-buttons">
        <button class="accent" @click="saveRoster">Save roster</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
em.aside.date {
  font-size: 11pt;
}
</style>
