<script setup lang="ts">
import AvailabilityGrid from "../components/AvailabilityGrid.vue";
import AvailabilityComboBox from "../components/AvailabilityComboBox.vue";
import WeekSelectionBox from "../components/WeekSelectionBox.vue";
import { computed, onMounted, reactive, ref } from "vue";
import { useTeamsStore } from "../stores/teams";
import { useScheduleStore } from "../stores/schedule";

const teams = useTeamsStore();
const schedule = useScheduleStore();

const options = ref([
  "TEAM PEPEJA forsenCD",
  "The Snus Brotherhood",
]);

const firstHour = computed(() => shouldShowAllHours.value ? 0 : 14);
const lastHour = computed(() => shouldShowAllHours.value ? 23 : 22);
const shouldShowAllHours = ref(false);

const comboBoxIndex = ref(0);

//const availability = reactive(new Array(168));
const availability = schedule.availability;

const selectionMode = ref(1);

const isEditing = ref(false);

function saveSchedule() {
  schedule.saveSchedule()
    .then(() => {
      isEditing.value = false;
    });
}

onMounted(() => {
  teams.fetchTeams()
    .then((teamsList) => {
      options.value = Object.values(teamsList);
      schedule.fetchSchedule()
        .then(() => {

        });
    })
});
</script>

<template>
  <main>
    <div class="schedule-view-container" v-if="options.length > 0">
      <div class="top-menu">
        <div class="subtext">
          Availability for
          <AvailabilityComboBox :options="options" v-model="comboBoxIndex" />
        </div>
        <div>
          <WeekSelectionBox
            v-model="schedule.dateStart"
            :is-disabled="isEditing" />
        </div>
      </div>
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
    <div v-else>
      You currently are not in any team to schedule for.
    </div>
  </main>
</template>

<style scoped>
.schedule-view-container {
  display: inline-block;
}

.top-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.button-group {
  display: flex;
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
  border-radius: 8px 0 0 8px;
}

button.right {
  border-radius: 0 8px 8px 0;
}
</style>
