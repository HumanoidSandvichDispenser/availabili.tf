<script setup lang="ts">
import AvailabilityGrid from "../components/AvailabilityGrid.vue";
import AvailabilityComboBox from "../components/AvailabilityComboBox.vue";
import WeekSelectionBox from "../components/WeekSelectionBox.vue";
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

onMounted(() => {
  teamsStore.fetchTeams()
    .then((teamsList) => {
      options.value = Object.values(teamsList.teams);
      // select team with id in query parameter if exists
      const queryTeam = teamsList.teams.find(x => x.id == route.query.teamId);
      if (queryTeam) {
        selectedTeam.value = queryTeam;
        schedule.team = queryTeam;
        schedule.fetchSchedule();
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
            label="team_name"
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
          <button v-else class="accent" @click="isEditing = true">
            <i class="bi bi-pencil-fill"></i>
          </button>
        </div>
      </div>
    </div>
    <div v-else>
      You currently are not in any team to schedule for.
    </div>
  </main>
</template>

<style scoped>
.schedule-view-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
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
  background-color: var(--accent-transparent);
}

button.left {
  border-radius: 4px 0 0 4px;
}

button.right {
  border-radius: 0 4px 4px 0;
}

.v-select {
  display: inline-block;
  width: auto;
  min-width: 11em;
}
</style>
