<script setup lang="ts">
import { useScheduleStore } from "../stores/schedule";
import { computed, type PropType } from "vue";
import { type AvailabilitySchema } from "@/client";

const scheduleStore = useScheduleStore();

const hoveredIndex = computed(() => scheduleStore.hoveredIndex);

const availabilityAtHoveredIndex = computed(() => {
  if (hoveredIndex.value) {
    return props.player?.availability[hoveredIndex.value] ?? 0;
  }
  return undefined;
});

const props = defineProps({
  player: Object as PropType<AvailabilitySchema>,
});

function onMouseOver() {
  scheduleStore.overlay = props.player;
}

function onMouseLeave() {
  if (scheduleStore.overlay == props.player) {
    scheduleStore.overlay = undefined;
  }
}
</script>

<template>
  <div
    class="player"
    @mouseover="onMouseOver(player)"
    @mouseleave="onMouseLeave"
  >
    <span v-if="availabilityAtHoveredIndex > 0">
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
  </div>
</template>

<style scoped>
.player:hover {
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
