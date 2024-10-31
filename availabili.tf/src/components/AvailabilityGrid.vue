<script setup lang="ts">
import { computed, defineModel, defineProps, reactive, ref, onMounted, onUnmounted } from "vue";

const model = defineModel();
const firstHour = 14;
const lastHour = 22;

const props = defineProps({
  selectionMode: Number,
  isDisabled: Boolean,
  dateStart: Date,
});

const selectionStart = reactive({ x: undefined, y: undefined });
const selectionEnd = reactive({ x: undefined, y: undefined });
const isCtrlDown = ref(false);
const isShiftDown = ref(false);

const lowerBoundX = computed(() => {
  return isShiftDown.value ? 0 :
    Math.min(selectionStart.x, selectionEnd.x)
});
const upperBoundX = computed(() => {
  return isShiftDown.value ? 7 :
    Math.max(selectionStart.x, selectionEnd.x)
});
const lowerBoundY = computed(() => {
  return isCtrlDown.value ? firstHour :
    Math.min(selectionStart.y, selectionEnd.y)
});
const upperBoundY = computed(() => {
  return isCtrlDown.value ? lastHour :
    Math.max(selectionStart.y, selectionEnd.y)
});

function selectionInside(dayIndex, hour) {
  if (selectionStart.x != undefined) {
    return (dayIndex >= lowerBoundX.value && dayIndex <= upperBoundX.value) &&
      (hour >= lowerBoundY.value && hour <= upperBoundY.value);
  }

  return false;
}

const days = computed(() => {
  let ret = [];
  for (let i = 0; i < 7; i++) {
    const date = new Date(props.dateStart);
    date.setDate(props.dateStart.getDate() + i);
    ret.push(date);
  }
  return ret;
});

const hours = computed(() => {
  return Array.from(Array(lastHour - firstHour + 1).keys())
    .map(x => x + firstHour);
});

const daysOfWeek = [
  "Sun",
  "Mon",
  "Tue",
  "Wed",
  "Thu",
  "Fri",
  "Sat"
];

const isMouseDown = ref(false);
const selectionValue = ref(0);

function onSlotMouseDown($event, x, y) {
  if (props.isDisabled) {
    return;
  }

  selectionValue.value = model.value[24 * x + y] == props.selectionMode ?
    0 : props.selectionMode;

  selectionStart.x = x;
  selectionStart.y = y;
  selectionEnd.x = x;
  selectionEnd.y = y;

  isShiftDown.value = $event.shiftKey;
  isCtrlDown.value = $event.ctrlKey;

  console.log("selected " + x + " " + y);
}

function onSlotMouseOver($event, x, y) {
  if (props.isDisabled) {
    return;
  }

  if ($event.buttons & 1 == 1) {
    isShiftDown.value = $event.shiftKey;
    isCtrlDown.value = $event.ctrlKey;

    selectionEnd.x = x;
    selectionEnd.y = y;
  }
}

function onSlotMouseUp($event) {
  if (props.isDisabled || selectionStart.x == undefined) {
    return;
  }

  for (let x = lowerBoundX.value; x <= upperBoundX.value; x++) {
    for (let y = lowerBoundY.value; y <= upperBoundY.value; y++) {
      model.value[24 * x + y] = selectionValue.value;
    }
  }

  selectionStart.x = undefined;
}

function onKeyUp($event) {
  switch ($event.key) {
    case "Shift":
      isShiftDown.value = false;
      break;
    case "Control":
      isCtrlDown.value = false;
      break;
  }
}

function onKeyDown($event) {
  switch ($event.key) {
    case "Shift":
      isShiftDown.value = true;
      break;
    case "Control":
      isCtrlDown.value = true;
      break;
  }
}
onMounted(() => {
  window.addEventListener("mouseup", onSlotMouseUp);
  window.addEventListener("keydown", onKeyDown);
  window.addEventListener("keyup", onKeyUp);
});

onUnmounted(() => {
  console.log("removing");
  window.removeEventListener("mouseup", onSlotMouseUp);
  window.removeEventListener("keydown", onKeyDown);
  window.removeEventListener("keyup", onKeyUp);
});

</script>

<template>
  <div class="grid">
    <div>
      <div class="height-48px"></div>
      <div class="height-24px hour-marker-container" v-for="hour, i in hours" :key="i">
        <span class="hour-marker" v-if="i % 2 == 0 || i == hours.length">
          {{ hour % 24 }}:30 / {{ (hour + 3) % 24 }}:30 EST
        </span>
      </div>
      <div class="height-24px hour-marker-container">
        <span class="hour-marker">
          {{ (lastHour + 1) % 24 }}:30 / {{ (lastHour + 4) % 24 }}:30 EST
        </span>
      </div>
    </div>
    <div v-for="(day, dayIndex) in days" :key="dayIndex" class="column">
      <div class="date">
        <div class="day-of-week">{{ daysOfWeek[day.getDay()] }}</div>
        <div class="day">{{ day.getDate() }}</div>
      </div>
      <div class="column-time-slots">
        <div
          :class="{
            'time-slot': true,
            'height-24px': true,
          }"
          :selection="
            selectionInside(dayIndex, hour) ? selectionValue
              : model[24 * dayIndex + hour]
          "
          v-for="hour in hours"
          @mousedown="onSlotMouseDown($event, dayIndex, hour)"
          @mouseover="onSlotMouseOver($event, dayIndex, hour)"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.height-24px {
  height: 24px;
}

.height-32px {
  height: 32px;
}

.height-48px {
  height: 48px;
}

.hour-marker-container {
  text-align: right;
}

.hour-marker {
  font-size: 12px;
  line-height: 0;
  position: relative;
  top: -0.75rem;
  margin-right: 8px;
  color: var(--subtext-0);
}

.grid {
  display: flex;
  user-select: none;
}

.grid > .column > .column-time-slots {
  width: 72px;
  border: 4px;
  border: 1px solid var(--text);
  border-left: none;
}

.grid > .column:nth-child(2) > .column-time-slots {
  border-left: 1px solid var(--text);
}

.date {
  display: flex;
  flex-direction: column;
  justify-content: end;
  text-align: center;
  height: 48px;
}

.date .day-of-week {
  color: var(--subtext-0);
  font-size: 12px;
  text-transform: uppercase;
  line-height: 0;
  margin-bottom: 2px;
}

.date .day {
  font-size: 20px;
  font-weight: 700;
}

.time-slot:hover {
  background-color: var(--crust);
  outline: 2px inset var(--subtext-0);
}

.time-slot:nth-child(2n):not(:last-child) {
  border-bottom: 1px dashed var(--text);
}

.time-slot[selection="1"] {
  background-color: var(--accent-transparent-50);
}

.time-slot[selection="2"] {
  background-color: var(--accent);
}
</style>
