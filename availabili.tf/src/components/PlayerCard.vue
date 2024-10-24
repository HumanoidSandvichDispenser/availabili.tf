<script setup lang="ts">
import type { PlayerTeamRole } from "../player";
import { computed, type PropType } from "vue";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const props = defineProps({
  roleTitle: String,
  player: Object as PropType<PlayerTeamRole>,
  isRoster: Boolean,
});

const isSelected = computed(() => {
  if (props.isRoster) {
    return rosterStore.selectedRole == props.roleTitle;
  }
  return Object.values(rosterStore.selectedPlayers).includes(props.player);
});

function onClick() {
  if (props.isRoster) {
    rosterStore.selectedRole = props.roleTitle;
  } else {
    // we are selecting the player
    rosterStore.selectPlayerForRole(props.player, props.roleTitle);
  }
};
</script>

<template>
  <button :class="{
    'player-card': true,
    'no-player': !player,
    'selected': isSelected,
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
  </button>
</template>

<style scoped>
.player-card {
  background-color: var(--crust);
  padding: 1em;
  border-radius: 8px;
  user-select: none;
}

.player-card:hover {
  background-color: var(--surface-0);
  transition-duration: 200ms;
}

.player-card.no-player {
  border: 2px dashed var(--overlay-0);
}

.player-card.no-player.selected {
  background-color: var(--accent-transparent);
  border: 2px dashed var(--accent);
  color: var(--accent);
}

.player-card.no-player:not(.selected) {
  background-color: transparent;
  color: var(--overlay-0);
}

.player-card.no-player:hover:not(.selected) {
  background-color: var(--surface-0);
}

.player-card.selected {
  border-color: var(--accent);
  border: 2px solid var(--accent);
  background-color: var(--accent-transparent);
  color: var(--accent);
}

h1 {
  font-size: 24px;
  font-weight: 700;
}
</style>
