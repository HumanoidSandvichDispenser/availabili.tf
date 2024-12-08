<script setup lang="ts">
import type { EventWithPlayerSchema, TeamSchema } from "@/client";
import EventCard from "./EventCard.vue";

const props = defineProps<{
  events: EventWithPlayerSchema[];
  teamContext: TeamSchema;
}>();
</script>

<template>
  <div class="events-list" v-if="props.events?.length > 0">
    <EventCard v-for="event in props.events" :key="event.event.id" :event="event" />
  </div>
  <div class="events-list" v-else>
    <em class="subtext">
      No upcoming events. Create one in the
      <router-link
        :to="{
          name: 'schedule',
          query: {
            teamId: props.teamContext.id
          }
        }"
      >
        schedule
      </router-link>
      page.
    </em>
  </div>
</template>

<style scoped>
.events-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
