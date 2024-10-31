<script setup lang="ts">
import AvailabilityGrid from "../components/AvailabilityGrid.vue";
import AvailabilityComboBox from "../components/AvailabilityComboBox.vue";
import WeekSelectionBox from "../components/WeekSelectionBox.vue";
import { reactive, ref } from "vue";
import { useScheduleStore } from "../stores/schedule.ts";

const schedule = useScheduleStore();

const options = reactive([
  "TEAM PEPEJA forsenCD",
  "The Snus Brotherhood",
]);

const comboBoxIndex = ref(0);

//const availability = reactive(new Array(168));
const availability = schedule.availability;

const selectionMode = ref(1);

const isEditing = ref(false);
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
          <WeekSelectionBox v-model="schedule.dateStart" />
        </div>
      </div>
      <AvailabilityGrid v-model="availability"
        :selection-mode="selectionMode"
        :is-disabled="!isEditing"
        :date-start="schedule.dateStart"
      />
      <div class="button-group">
        <button>Show all times</button>
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
          <button @click="isEditing = false">
            <i class="bi bi-check-circle-fill"></i>
            Save
          </button>
        </template>
        <button v-else class="accent" @click="isEditing = true">
          <i class="bi bi-pencil-fill"></i>
          Edit
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
