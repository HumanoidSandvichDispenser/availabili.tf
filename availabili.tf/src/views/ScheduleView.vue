<script setup lang="ts">
import AvailabilityGrid from "../components/AvailabilityGrid.vue";
import AvailabilityComboBox from "../components/AvailabilityComboBox.vue";
import WeekSelectionBox from "../components/WeekSelectionBox.vue";
import SchedulePlayerList from "../components/SchedulePlayerList.vue";
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useTeamsStore } from "../stores/teams";
import { useScheduleStore } from "../stores/schedule";
import { useRoute, useRouter } from "vue-router";

const teamsStore = useTeamsStore();
const schedule = useScheduleStore();
const router = useRouter();
const route = useRoute();

const options = ref([ ]);

const firstHour = computed(() => shouldShowAllHours.value ? 0 : 14);
const lastHour = computed(() => shouldShowAllHours.value ? 23 : 22);
const shouldShowAllHours = ref(false);

const comboBoxIndex = ref(0);

const availability = schedule.availability;

const selectionMode = ref(1);

const selectedTime = ref(undefined);

const availabilityOverlay = computed(() => schedule.overlay?.availability);

const isEditing = ref(false);

const selectedTeam = ref();

watch(selectedTeam, (newTeam) => {
  if (newTeam) {
    schedule.team = newTeam;
  }
});

function saveSchedule() {
  schedule.saveSchedule()
    .then(() => {
      isEditing.value = false;
    });
}

function copyPreviousWeek() {
  schedule.fetchSchedule(schedule.dateStart.clone().add(-7, "days"))
    .then((response) => {
      schedule.saveSchedule();
      return response;
    });
}

onMounted(() => {
  teamsStore.fetchTeams()
    .then((teamsList) => {
      options.value = Object.values(teamsList.teams);

      // select team with id in query parameter if exists
      const queryTeam = teamsList.teams.find(x => x.id == route.query.teamId);
      if (queryTeam) {
        selectedTeam.value = queryTeam;
        schedule.team = queryTeam;
      } else {
        selectedTeam.value = options.value[0];
      }
    });
});
</script>

<template>
  <main>
    <div class="schedule-view-container" v-if="options.length > 0">
      <div class="top-menu">
        <div class="subtext">
          Availability for
          <v-select
            :options="options"
            label="teamName"
            v-model="selectedTeam"
          />
        </div>
        <div>
          <WeekSelectionBox
            v-model="schedule.dateStart"
            :is-disabled="isEditing" />
        </div>
      </div>
      <div class="grid-container">
        <AvailabilityGrid v-model="availability"
          v-model:selectedTime="selectedTime"
          v-model:hoveredIndex="schedule.hoveredIndex"
          :overlay="availabilityOverlay"
          :selection-mode="selectionMode"
          :is-disabled="!isEditing"
          :date-start="schedule.dateStart"
          :first-hour="firstHour"
          :last-hour="lastHour"
        />
        <div class="button-group">
          <button v-if="shouldShowAllHours" @click="shouldShowAllHours = false">
            Show designated times
          </button>
          <button v-else @click="shouldShowAllHours = true">
            Show all times
          </button>
          <template v-if="isEditing">
            <div class="radio-group">
              <button
                :class="{ 'radio': true, 'selected': selectionMode == 1, 'left': true }"
                @click="selectionMode = 1"
              >
                Available if needed
              </button>
              <button
                :class="{ 'radio': true, 'selected': selectionMode == 2, 'right': true }"
                @click="selectionMode = 2"
              >
                Definitely available
              </button>
            </div>
            <button @click="saveSchedule()">
              <i class="bi bi-check-circle-fill"></i>
            </button>
          </template>
          <template v-else>
            <button @click="copyPreviousWeek">
              Copy previous week
            </button>
            <button class="accent" @click="isEditing = true">
              <i class="bi bi-pencil-fill"></i>
            </button>
          </template>
        </div>
      </div>
    </div>
    <div v-else>
      You currently are not in any team to schedule for.
    </div>
    <div class="player-list">
      <SchedulePlayerList
        :selected-time="selectedTime"
      />
    </div>
  </main>
</template>

<style scoped>
main {
  flex-direction: row;
  display: flex;
  justify-content: space-evenly;
}

.schedule-view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.top-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.grid-container {
  display: inline-flex;
  flex-direction: column;
  align-content: center;
}

.button-group {
  display: inline-flex;
  gap: 8px;
  justify-content: end;
}

.radio-group {
  display: flex;
  gap: 2px;
}

button.radio {
  font-weight: 500;
}

button.radio:hover {
  font-weight: 500;
}

button.radio.selected {
  color: var(--accent);
  color: var(--accent-transparent);
}

button.left {
  border-radius: 4px 0 0 4px;
}

button.radio.left.selected {
  color: var(--yellow);
  background-color: var(--yellow-transparent);
}

button.right {
  border-radius: 0 4px 4px 0;
}

button.right.radio.selected {
  color: var(--green);
  background-color: var(--green-transparent);
}

.v-select {
  display: inline-block;
  width: auto;
  min-width: 11em;
}

.schedule-view-container {
  flex-basis: 75%;
}

.player-list {
  flex-basis: 25%;
}
</style>
