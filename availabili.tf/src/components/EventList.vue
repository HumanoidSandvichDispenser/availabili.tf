<script setup lang="ts">
import type { EventWithPlayerSchema } from "@/client";
import EventCard from "./EventCard.vue";

const props = defineProps<{
  events: EventWithPlayerSchema[];
}>();
</script>

<template>
  <div class="events-list" v-if="props.events?.length > 0">
    <EventCard v-for="event in props.events" :key="event.event.id" :event="event" />
  </div>
  <div class="events-list" v-else>
    <em class="subtext">No upcoming events.</em>
  </div>
</template>

<style scoped>
.events-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
