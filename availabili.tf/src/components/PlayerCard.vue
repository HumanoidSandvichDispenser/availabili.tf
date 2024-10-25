<script setup lang="ts">
import type { PlayerTeamRole } from "../player";
import { computed, type PropType } from "vue";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const props = defineProps({
  roleTitle: String,
  player: Object as PropType<PlayerTeamRole>,
  isRoster: Boolean,
  isRinger: Boolean,
});

const isSelected = computed(() => {
  if (props.isRoster) {
    return rosterStore.selectedRole == props.roleTitle;
  }

  if (props.isRinger) {
    return rosterStore.selectedPlayers[props.roleTitle]?.playtime == -1;
  }

  return Object.values(rosterStore.selectedPlayers).includes(props.player);
});

function onClick() {
  if (props.isRoster) {
    if (rosterStore.selectedRole == props.roleTitle) {
      rosterStore.selectedRole = undefined;
    } else {
      rosterStore.selectedRole = props.roleTitle;
    }
  } else {
    // we are selecting the player
    if (isSelected.value) {
      rosterStore.selectPlayerForRole(undefined, props.roleTitle);
    } else {
      if (props.isRinger) {
        const ringerPlayer: PlayerTeamRole = {
          steamId: -1,
          name: "Ringer",
          role: props.roleTitle,
          main: false,
          availability: 1,
          playtime: -1,
        };
        rosterStore.selectPlayerForRole(ringerPlayer, props.roleTitle);
      } else {
        rosterStore.selectPlayerForRole(props.player, props.roleTitle);
      }
    }
  }
};
</script>

<template>
  <button :class="{
    'player-card': true,
    'no-player': !player && !isRinger,
    'selected': isSelected,
    'can-be-available': player?.availability == 2
  }" @click="onClick">
    <div class="role-icon">
      <i :class="rosterStore.roleIcons[roleTitle]" />
    </div>
    <div v-if="player" class="role-info">
      <span>
        <h4 class="player-name">{{ player.name }}</h4>
        <span v-if="roleTitle != player.role">
          Subbing in as
        </span>
        {{ player.role }}
        <span v-if="!player.main && isRoster">
          (alternate)
        </span>
      </span>
    </div>
    <div v-else-if="isRinger" class="role-info">
      <span>
        <h4 class="player-name">Ringer</h4>
        {{ roleTitle }}
      </span>
    </div>
    <div v-else class="role-info">
      <span>
        {{ roleTitle }}
      </span>
    </div>
  </button>
</template>

<style scoped>
.player-card {
  background-color: white;
  padding: 1em;
  border-radius: 8px;
  user-select: none;
  display: flex;
  gap: 1em;
  align-items: center;
  border: 2px solid white;
  box-shadow: 1px 1px 8px var(--surface-0);
}

.player-card.can-be-available {
  color: var(--overlay-0);
}

.player-card .role-icon {
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 2em;
}

.player-card .role-info {
  text-align: left;
}

.player-card:hover {
  background-color: var(--surface-0);
  transition-duration: 200ms;
  border-color: var(--surface-0);
}

.player-card.no-player {
  border: 2px solid var(--overlay-0);
  box-shadow: none;
}

.player-card.no-player.selected {
  background-color: var(--accent-transparent);
  border: 2px solid var(--accent);
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

.player-name {
  font-size: 16px;
  font-weight: 600;
}
</style>
