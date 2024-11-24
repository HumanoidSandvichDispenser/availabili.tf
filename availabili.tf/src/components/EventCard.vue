<script setup lang="ts">
import type { EventSchema } from "@/client";
import { useTeamsStore } from "@/stores/teams";
import moment from "moment";
import { computed } from "vue";

const teamsStore = useTeamsStore();

const date = computed(() => moment(props.event.startTime));

const formattedTime = computed(() => {
  const team = teamsStore.teams[props.event.teamId];
  const offsetDate = date.value.clone().tz(team.tzTimezone);
  return `${date.value.format("LT")} (${offsetDate.format("LT z")})`;
});

const day = computed(() => {
  return date.value.format("D");
});

const shortMonth = computed(() => {
  return date.value.format("MMM");
});

const props = defineProps<{
  event: EventSchema;
}>();
</script>

<template>
  <div class="event-card">
    <div class="date">
      <span class="month">
        {{ shortMonth }}
      </span>
      <span class="day">
        {{ day }}
      </span>
    </div>
    <div class="details">
      <div>
        <h3>{{ event.name }}</h3>
        <div>
          <span v-if="event.description">{{ event.description }}</span>
          <em v-else class="subtext">No description provided.</em>
        </div>
      </div>
      <div class="subdetails">
        <span>
          <i class="bi bi-clock-fill margin" />
          {{ formattedTime }}
        </span>
        <span class="class-info">
          <i class="tf2class tf2-PocketScout margin" />
          Pocket Scout
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.event-card {
  display: flex;
  padding: 1rem;
  align-items: center;
  /*background-color: white;*/
  border: 1px solid var(--text);
  border-radius: 8px;
  align-items: stretch;
}

.date {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1;
  flex-basis: 4rem;
}

.date .month {
  text-transform: uppercase;
  font-weight: 600;
  font-size: 0.8rem;
}

.date .day {
  font-size: 1.5rem;
  font-weight: 700;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.subdetails {
  display: flex;
  flex-direction: column;
}

.subdetails .margin {
  margin-right: 0.25em;
}

.subdetails i.tf2class {
  line-height: 1em;
  font-size: 1.2rem;
  vertical-align: middle;
}
</style>
