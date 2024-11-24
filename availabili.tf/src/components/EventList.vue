<script setup lang="ts">
import type { EventSchema } from "@/client";
import EventCard from "./EventCard.vue";

const props = defineProps<{
  events: EventSchema[];
}>();
</script>

<template>
  <h2>Upcoming Events</h2>
  <div class="events-list">
    <EventCard v-for="event in props.events" :key="event.id" :event="event" />
  </div>
</template>

<style scoped>
h2 {
  margin-bottom: 1rem;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
