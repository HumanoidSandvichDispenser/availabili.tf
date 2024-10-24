<script setup lang="ts">
import type { PlayerTeamRole } from "../player";
import type { PropType } from "vue";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const props = defineProps({
  roleTitle: String,
  player: Object as PropType<PlayerTeamRole>,
  isRoster: Boolean,
});

function onClick() {
  if (props.isRoster) {
    rosterStore.selectedRole = props.roleTitle;
  }
};
</script>

<template>
  <div :class="{
    'player-card': true,
    'no-player': !player,
    'selected': rosterStore.selectedRole == roleTitle && isRoster
  }" @click="onClick">
    <div v-if="player">
      <h1>{{ player.name }}</h1>
      <span v-if="roleTitle != player.role">
        Subbing in as
      </span>
      {{ player.role }}
      <span v-if="!player.main">
        (alternate role)
      </span>
    </div>
    <div v-else>
      {{ roleTitle }}
    </div>
  </div>
</template>

<style scoped>
.player-card {
  background-color: var(--crust);
  padding: 1em;
  border-radius: 8px;
  user-select: none;
}

.player-card:hover {
  background-color: var(--overlay-0);
  transition-duration: 200ms;
}

.player-card.no-player {
  border: 2px solid var(--overlay-0);
}

.player-card.no-player:not(.selected) {
  background-color: transparent;
  color: var(--overlay-0);
}

.player-card.no-player:hover:not(.selected) {
  background-color: var(--surface-0);
}

.player-card.selected {
  background-color: var(--flamingo);
  border-color: var(--flamingo);
  color: var(--crust);
}

h1 {
  font-size: 24px;
}
</style>
