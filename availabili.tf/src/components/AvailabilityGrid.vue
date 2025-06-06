<script setup lang="ts">
import { computed, defineModel, defineProps, reactive, ref, onMounted, onUnmounted } from "vue";
import { type Moment } from "moment";
import { useScheduleStore } from "../stores/schedule";

const scheduleStore = useScheduleStore();

const model = defineModel<number[]>({ required: true });

const selectedTime = defineModel("selectedTime");
const selectedIndex = defineModel("selectedIndex");

const hoveredIndex = defineModel("hoveredIndex");

const props = withDefaults(defineProps<{
  selectionMode: number,
  isDisabled: boolean,
  overlay: number[] | undefined,
  dateStart: Moment,
  firstHour: number,
  lastHour: number
}>(), {
  firstHour: 14,
  lastHour: 22
});

const isEditing = computed(() => !props.isDisabled);

type Coordinate = {
  x?: number,
  y?: number
};

const selectionStart = reactive<Coordinate>({ x: undefined, y: undefined });
const selectionEnd = reactive<Coordinate>({ x: undefined, y: undefined });
const isCtrlDown = ref(false);
const isShiftDown = ref(false);

const lowerBoundX = computed(() => {
  return isShiftDown.value ? 0 :
    Math.min(selectionStart.x ?? NaN, selectionEnd.x ?? NaN)
});
const upperBoundX = computed(() => {
  return isShiftDown.value ? 6 :
    Math.max(selectionStart.x ?? NaN, selectionEnd.x ?? NaN)
});
const lowerBoundY = computed(() => {
  return isCtrlDown.value ? props.firstHour :
    Math.min(selectionStart.y ?? NaN, selectionEnd.y ?? NaN)
});
const upperBoundY = computed(() => {
  return isCtrlDown.value ? props.lastHour :
    Math.max(selectionStart.y ?? NaN, selectionEnd.y ?? NaN)
});

function selectionInside(dayIndex: number, hour: number) {
  if (selectionStart.x != undefined) {
    return (dayIndex >= lowerBoundX.value && dayIndex <= upperBoundX.value) &&
      (hour >= lowerBoundY.value && hour <= upperBoundY.value);
  }

  return false;
}

const days = computed(() => {
  let ret = [0, 1, 2, 3, 4, 5, 6];
  //for (let i = 0; i < 7; i++) {
  //  const date = new Date(props.dateStart);
  //  date.setDate(props.dateStart.getDate() + i);
  //  ret.push(date);
  //}
  return ret
    .map((val) => props.dateStart.clone().add(val, "days"));
});

const hours = computed(() => {
  return Array.from(Array(props.lastHour - props.firstHour + 1).keys())
    .map(x => x + props.firstHour);
});

function getTimeAtCell(dayIndex: number, hour: number) {
  return props.dateStart.clone()
    .add(dayIndex, "days")
    .add(hour, "hours");
}

function onSlotMouseOver($event: MouseEvent, x: number, y: number) {
  hoveredIndex.value = 24 * x + y;

  if (!isEditing.value) {
    return;
  }

  if (($event.buttons & 1) == 1) {
    isShiftDown.value = $event.shiftKey;
    isCtrlDown.value = $event.ctrlKey;

    selectionEnd.x = x;
    selectionEnd.y = y;
  }
}

function onSlotMouseLeave(_: MouseEvent, x: number, y: number) {
  let index = 24 * x + y;
  if (hoveredIndex.value == index) {
    hoveredIndex.value = undefined;
  }
}

const selectionValue = ref(0);

function onSlotMouseDown($event: MouseEvent, x: number, y: number) {
  if (!isEditing.value) {
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

function onSlotMouseUp(_: MouseEvent) {
  if (!isEditing.value || selectionStart.x == undefined) {
    return;
  }

  for (let x = lowerBoundX.value; x <= upperBoundX.value; x++) {
    for (let y = lowerBoundY.value; y <= upperBoundY.value; y++) {
      model.value[24 * x + y] = selectionValue.value;
    }
  }

  selectionStart.x = undefined;
}

function onSlotClick(dayIndex: number, hour: number) {
  let index = dayIndex * 24 + hour;

  if (isEditing.value) {
    return;
  }

  if (selectedIndex.value == index) {
    selectedIndex.value = -1;
    selectedTime.value = undefined;
    return;
  }

  selectedTime.value = getTimeAtCell(dayIndex, hour);
  selectedIndex.value = index;
  scheduleStore.selectIndex(24 * dayIndex + hour);
}

function onKeyUp($event: KeyboardEvent) {
  switch ($event.key) {
    case "Shift":
      isShiftDown.value = false;
      break;
    case "Control":
      isCtrlDown.value = false;
      break;
  }
}

function onKeyDown($event: KeyboardEvent) {
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

function getAvailabilityCell(day: number, hour: number) {
  let index = day * 24 + hour;
  if (props.overlay && props.overlay[index] != undefined) {
    return props.overlay[index]
  }
  return model.value[index];
}

const currentTimezone = computed(() =>
  Intl.DateTimeFormat().resolvedOptions().timeZone);

function getHour(offset: number, tz?: string) {
  let time = props.dateStart.clone()
  if (tz) {
    time = time.tz(tz);
  }
  return time.add(offset, "hours");
}
</script>

<template>
  <div class="grid">
    <div>
      <div class="height-48px"></div>
      <div class="height-24px hour-marker-container" v-for="hour, i in hours" :key="i">
        <span class="hour-marker" v-if="i % 2 == 0 || i == hours.length">
          {{ getHour(hour).format("HH:mm z") }}
          <span v-if="scheduleStore.team.tzTimezone != currentTimezone">
            / {{ getHour(hour, scheduleStore.team.tzTimezone).format("HH:mm z") }}
          </span>
        </span>
      </div>
      <div class="height-24px hour-marker-container">
        <span class="hour-marker">
          {{ getHour(lastHour + 1).format("HH:mm z") }}
          <span v-if="scheduleStore.team.tzTimezone != currentTimezone">
            / {{ getHour(lastHour + 1, scheduleStore.team.tzTimezone).format("HH:mm z") }}
          </span>
        </span>
      </div>
    </div>
    <div v-for="(day, dayIndex) in days" :key="dayIndex" class="column">
      <div class="date">
        <div class="day-of-week">{{ day.format("ddd") }}</div>
        <div class="day">{{ day.date() }}</div>
      </div>
      <div class="column-time-slots">
        <div
          :class="{
            'time-slot': true,
            'height-24px': true,
            'selected': selectedIndex == 24 * dayIndex + hour,
          }"
          :selection="
            selectionInside(dayIndex, hour) ? selectionValue
              : getAvailabilityCell(dayIndex, hour)
          "
          v-for="hour in hours"
          @mousedown="onSlotMouseDown($event, dayIndex, hour)"
          @mouseover="onSlotMouseOver($event, dayIndex, hour)"
          @mouseleave="onSlotMouseLeave($event, dayIndex, hour)"
          @click="onSlotClick(dayIndex, hour)"
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
  display: inline-flex;
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

.time-slot:hover, .time-slot.selected {
  outline: 2px inset var(--subtext-0);
}

.time-slot.selected {
  outline-style: solid;
  animation: pulse 1s infinite;
}

.time-slot.selected:hover {
  outline-style: solid;
}

@keyframes pulse {
  0% {
    outline-color: var(--overlay-0);
  }
  50% {
    outline-color: var(--text);
  }
  100% {
    outline-color: var(--overlay-0);
  }
}

.time-slot:hover {
  background-color: var(--crust);
  outline-style: dashed;
}

.time-slot:nth-child(2n):not(:last-child) {
  border-bottom: 1px dashed var(--text);
}

.time-slot[selection="1"] {
  /*background-color: var(--accent-transparent-50);*/
  background-color: var(--yellow-transparent);
}

.time-slot[selection="2"] {
  /*background-color: var(--accent);*/
  background-color: var(--green-transparent);
}
</style>
