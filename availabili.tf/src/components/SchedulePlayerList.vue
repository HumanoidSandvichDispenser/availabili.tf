<script setup lang="ts">
import { useScheduleStore } from "../stores/schedule";
import SchedulePlayerListItem from "./SchedulePlayerListItem.vue";

const scheduleStore = useScheduleStore();
</script>

<template>
  <div class="schedule-player-list">
    <h3>{{ scheduleStore.team?.teamName }}</h3>
    <SchedulePlayerListItem
      v-for="record in scheduleStore.playerAvailability"
      :player="record"
    />
  </div>
</template>

<style scoped>
h3 {
  font-weight: 700;
}

.player:hover {
  background-color: var(--mantle);
}
</style>
