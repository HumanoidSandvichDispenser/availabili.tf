<script setup lang="ts">
import { useScheduleStore } from "../stores/schedule";
import { computed, type PropType } from "vue";
import { type AvailabilitySchema } from "@/client";

const scheduleStore = useScheduleStore();

const hoveredIndex = computed(() => scheduleStore.hoveredIndex);

const availabilityAtHoveredIndex = computed(() => {
  if (hoveredIndex.value && props.player?.availability) {
    return props.player.availability[hoveredIndex.value] ?? 0;
  }
  return undefined;
});

const props = defineProps({
  player: Object as PropType<AvailabilitySchema>,
});

function onMouseOver() {
  if (props.player) {
    scheduleStore.hoveredMember = props.player;
  }
}

function onMouseLeave() {
  if (scheduleStore.hoveredMember == props.player) {
    scheduleStore.hoveredMember = undefined;
  }
}
</script>

<template>
  <div
    class="player"
    v-if="player"
    @mouseover="onMouseOver"
    @mouseleave="onMouseLeave"
  >
    <input
      class="player-checkbox"
      type="checkbox"
      v-model="scheduleStore.selectedMembers[player.steamId]"
      :value="player"
      :id="player.steamId"
    />
    <label
      :for="player.steamId"
    >
      <span v-if="availabilityAtHoveredIndex ?? 0 > 0">
        <span v-if="availabilityAtHoveredIndex == 1" class="can-be-available">
          {{ player.username }}
        </span>
        <span v-else class="available">
          {{ player.username }}
        </span>
      </span>
      <s v-else-if="availabilityAtHoveredIndex == 0">
        {{ player.username }}
      </s>
      <span v-else>
        {{ player.username }}
      </span>
    </label>
  </div>
</template>

<style scoped>
input {
  display: inline-block;
  width: unset;
}

.player {
  display: flex;
  gap: 4px;
  padding: 6px 8px;
  border-radius: 4px;
}

.player label {
  flex-grow: 1;
}

.player label:hover {
  background-color: var(--mantle);
}

.player span.can-be-available {
  background-color: var(--yellow-transparent);
}

.player span.available {
  background-color: var(--green-transparent);
}

.player s {
  color: var(--overlay-0);
}
</style>
