<script setup lang="ts">
import { useScheduleStore } from "../stores/schedule";
import SchedulePlayerListItem from "./SchedulePlayerListItem.vue";
import { useRouter } from "vue-router";
import { computed } from "vue";

const scheduleStore = useScheduleStore();

const router = useRouter();

const selectedTimeTz = computed(() =>
  props.selectedTime?.clone().tz(scheduleStore.team?.tzTimezone));

const isTeamTzLocal = computed(() => {
  return selectedTimeTz.value?.utcOffset() == props.selectedTime?.utcOffset();
});

//const props = defineProps({
//  selectedTime: Object
//});

const props = defineProps<{
  selectedTime?: moment.Moment;
  selectedIndex?: number;
}>();

function scheduleRoster() {
  if (!props.selectedTime) {
    return;
  }

  router.push({
    name: "roster-builder",
    params: {
      teamId: scheduleStore.team.id,
      startTime: props.selectedTime.unix(),
    }
  });
}
</script>

<template>
  <div class="schedule-player-list">
    <h3>{{ scheduleStore.team?.teamName }}</h3>
    <div class="list">
      <SchedulePlayerListItem
        v-for="record in scheduleStore.playerAvailability"
        :player="record"
      />
    </div>
    <h4 v-if="selectedTime">
      <div>
        {{ selectedTime.format("L LT z") }}
      </div>
      <div v-if="!isTeamTzLocal">
        {{ selectedTimeTz?.format("L LT z") }}
      </div>
    </h4>
    <button @click="scheduleRoster" v-if="selectedTime">
      Schedule for {{ selectedTime.format("L LT") }}
    </button>
    <div v-else class="subtext">
      <em>Select a time to schedule</em>
    </div>
  </div>
</template>

<style scoped>
h3, h4 {
  font-weight: 700;
}

h4, h4 > div {
  font-weight: 700;
  font-size: 10pt;
  min-height: 1em;
}

.schedule-player-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.player:hover {
  background-color: var(--mantle);
}

.list {
  display: flex;
  flex-direction: column;
}
</style>
