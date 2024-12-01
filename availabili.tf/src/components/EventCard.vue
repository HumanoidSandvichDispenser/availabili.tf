<script setup lang="ts">
import type { EventSchema, EventWithPlayerSchema } from "@/client";
import { useRosterStore } from "@/stores/roster";
import { useTeamsStore } from "@/stores/teams";
import { useTeamsEventsStore } from "@/stores/teams/events";
import moment from "moment";
import { computed } from "vue";
import EventCardDropdown from "./EventCardDropdown.vue";
import EventConfirmButton from "./EventConfirmButton.vue";
const teamsStore = useTeamsStore();
const rosterStore = useRosterStore();
const teamEventsStore = useTeamsEventsStore();

const date = computed(() => moment(props.event.event.startTime));

const formattedTime = computed(() => {
  const team = teamsStore.teams[props.event.event.teamId];
  const offsetDate = date.value.clone().tz(team.tzTimezone);
  return `${date.value.format("LT")} (${offsetDate.format("LT z")})`;
});

const day = computed(() => {
  return date.value.format("D");
});

const shortMonth = computed(() => {
  return date.value.format("MMM");
});

const teamId = computed(() => props.event.event.teamId);

const props = defineProps<{
  event: EventWithPlayerSchema;
}>();

function deleteEvent() {
  teamEventsStore.deleteEvent(props.event.event.id)
    .then(() => {
      // remove event from list
      // TODO: move this to the store
      let idx = teamEventsStore.teamEvents[teamId.value].indexOf(props.event);
      teamEventsStore.teamEvents[teamId.value].splice(idx, 1);
    });
}

function attend() {
  teamEventsStore.attendEvent(props.event.event.id);
}

function pending() {
  console.log("pending");
  teamEventsStore.attendEvent(props.event.event.id, false);
}

function unattend() {
  teamEventsStore.unattendEvent(props.event.event.id);
}
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
        <div class="header">
          <h3>{{ event.event.name }}</h3>
          <EventCardDropdown :event="event" @deleteEvent="deleteEvent" />
        </div>
        <div>
          <span>
            <i class="bi bi-clock-fill margin" />
            {{ formattedTime }}
          </span>
        </div>
      </div>
      <div class="subdetails">
        <span v-if="event.event.description">{{ event.event.description }}</span>
        <em v-else class="subtext">No description provided.</em>
      </div>
      <div class="button-group">
        <EventConfirmButton
          :playerEvent="event.playerEvent"
          @attend="attend"
          @pending="pending"
          @unattend="unattend"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
h3 {
  display: inline-block;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14pt;
}

.event-card {
  display: flex;
  align-items: center;
  /*background-color: white;*/
  align-items: stretch;
}

.date {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1;
  flex-basis: 4rem;
  padding: 1rem;
  background-color: var(--text);
  color: var(--base);
  border-radius: 8px 0 0 8px;
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
  padding: 1rem;
  border: 1px solid var(--text);
  border-radius: 0 8px 8px 0;
  display: flex;
  flex-direction: column;
  width: 100%;
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

.button-group {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
