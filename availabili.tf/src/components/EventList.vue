<script setup lang="ts">
import type { EventWithPlayerSchema, TeamSchema } from "@/client";
import EventCard from "./EventCard.vue";
import { onMounted, ref } from "vue";
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { useTeamsEventsStore } from "@/stores/teams/events";
import LoaderContainer from "./LoaderContainer.vue";
import { computed } from "@vue/reactivity";

const { teamId, team } = useTeamDetails();

const teamsStore = useTeamsStore();
const teamsEventsStore = useTeamsEventsStore();
const isLoading = ref(false);
const events = computed(() => teamsEventsStore.teamEvents[teamId.value]);

onMounted(() => {
  isLoading.value = true;
  teamsStore.fetchTeam(teamId.value)
    .then(() => {
      teamsEventsStore.fetchTeamEvents(teamId.value)
        .finally(() => isLoading.value = false);
    });
});
</script>

<template>
  <LoaderContainer v-if="isLoading" height="160">
    <rect x="0" y="0" rx="4" ry="4" width="100%" height="160" />
  </LoaderContainer>
  <div class="events-list" v-else-if="events?.length > 0">
    <EventCard v-for="event in events" :key="event.event.id" :event="event" />
  </div>
  <div class="events-list" v-else>
    <em class="subtext">
      No upcoming events. Create one in the
      <router-link
        :to="{
          name: 'schedule',
          query: {
            teamId,
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
