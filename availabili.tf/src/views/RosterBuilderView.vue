<script setup lang="ts">
import PlayerCard from "../components/PlayerCard.vue";
import { computed, reactive, onMounted, ref } from "vue";
import { useRosterStore } from "../stores/roster";
import { useRoute } from "vue-router";
import moment from "moment";
import { useEventsStore } from "@/stores/events";
import EventSchedulerForm from "@/components/EventSchedulerForm.vue";
import { useEventForm } from "@/composables/event-form";
import Loader from "@/components/Loader.vue";
import LoaderContainer from "@/components/LoaderContainer.vue";

const rosterStore = useRosterStore();
const eventsStore = useEventsStore();

const route = useRoute();

const isLoading = ref(false);

const hasAvailablePlayers = computed(() => {
  return rosterStore.availablePlayerRoles.length > 0;
});

const hasAlternates = computed(() => {
  return rosterStore.alternateRoles.length > 0;
});

const { eventId } = useEventForm();

function closeSelection() {
  rosterStore.selectedRole = undefined;
}

onMounted(async () => {
  isLoading.value = true;

  if (eventId.value) {
    const event = await eventsStore.fetchEvent(eventId.value);
    rosterStore.startTime = moment(event.startTime).unix();
    rosterStore.title = event.name;
    rosterStore.description = event.description;
    Object.assign(rosterStore.selectedPlayers, { });
    rosterStore.fetchPlayersFromEvent(eventId.value)
      .then(() => {
        isLoading.value = false;
      });
  } else {
    rosterStore.startTime = Number(route.params.startTime);
    rosterStore.fetchAvailablePlayers(rosterStore.startTime, Number(route.params.teamId))
      .then(() => {
        isLoading.value = false;
      });
  }
});
</script>

<template>
  <main v-if="isLoading">
    <LoaderContainer />
  </main>
  <main v-else>
    <div class="top">
      <a>
        <i class="bi bi-arrow-left" />
        Back
      </a>
    </div>
    <div class="columns">
      <div class="form-group margin column">
        <PlayerCard v-for="role in rosterStore.neededRoles"
                    :player="rosterStore.selectedPlayers[role]"
                    :role-title="role"
                    is-roster />
      </div>
      <div class="form-group margin column" v-if="rosterStore.selectedRole">
        <PlayerCard v-for="player in rosterStore.mainRoles"
                    :player="player"
                    :role-title="player.role" />
        <span v-if="!hasAvailablePlayers && rosterStore.selectedRole">
          No players are currently available for this role.
        </span>
        <h3 v-if="hasAvailablePlayers">Alternates</h3>
        <PlayerCard v-for="player in rosterStore.alternateRoles"
                    :player="player"
                    :role-title="player.role" />
        <PlayerCard v-if="rosterStore.selectedRole"
                    is-ringer
                    :role-title="rosterStore.selectedRole" />
        <div class="action-buttons">
          <button class="accent" @click="closeSelection">
            <i class="bi bi-check" />
            Done
          </button>
        </div>
      </div>
      <div class="column" v-else>
        <EventSchedulerForm />
      </div>
    </div>
  </main>
</template>

<style scoped>
.top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.top .button-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.columns {
  display: flex;
  flex-direction: row;
}

.column {
  display: flex;
  flex-grow: 1;
  margin-left: 4em;
  margin-right: 4em;
  flex-direction: column;
  row-gap: 8px;
  width: 100%;
}

.column h3 {
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  color: var(--overlay-0);
}

.roster-title {
  display: flex;
  gap: 0.5em;
}
</style>
