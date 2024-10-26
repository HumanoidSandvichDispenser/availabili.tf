<script setup lang="ts">
import AvailabilityGrid from "../components/AvailabilityGrid.vue";
import AvailabilityComboBox from "../components/AvailabilityComboBox.vue";
import WeekSelectionBox from "../components/WeekSelectionBox.vue";
import { reactive, ref } from "vue";

const options = reactive([
  "Team pepeja",
  "Snus Brotherhood",
]);

const comboBoxIndex = ref(0);

const availability = reactive(new Array(168));

const selectionMode = ref(1);
</script>

<template>
  <main>
    <div v-if="options.length > 0">
      <div>
        Availability for
        <AvailabilityComboBox :options="options" v-model="comboBoxIndex" />
        <WeekSelectionBox />
      </div>
      <AvailabilityGrid v-model="availability" :selection-mode="selectionMode" />
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
    </div>
    <div v-else>
      You currently are not in any team to schedule for.
    </div>
  </main>
</template>

<style scoped>
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
