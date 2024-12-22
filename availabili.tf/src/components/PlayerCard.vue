<script setup lang="ts">
import type { PlayerTeamRoleFlat } from "../player";
import { computed, type PropType } from "vue";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const props = withDefaults(defineProps<{
  roleTitle: string,
  player: PlayerTeamRoleFlat | undefined,
  isRoster: boolean,
}>(), {
  isRoster: false,
});

const isSelected = computed(() => {
  if (props.isRoster) {
    return rosterStore.selectedRole == props.roleTitle;
  }

  const selectedPlayers = rosterStore.selectedPlayers;

  return selectedPlayers[props.roleTitle]?.steamId == props.player?.steamId;
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
      rosterStore.selectPlayerForRole(props.player, props.roleTitle);
    }
  }
};

const playtime = computed(() => {
  let hours = props.player?.playtime ?? 0 / 3600;
  return hours.toFixed(1);
});
</script>

<template>
  <button :class="{
    'player-card': true,
    'no-player': !player,
    'selected': isSelected,
    'can-be-available': player?.availability == 1
  }" @click="onClick">
    <div class="role-icon">
      <i :class="rosterStore.roleIcons[roleTitle]" />
    </div>
    <div v-if="player" class="role-info">
      <span>
        <h4 class="player-name">{{ player.name }}</h4>
        <div class="subtitle">
          <span>
            {{ rosterStore.roleNames[player.role] }}
            <span v-if="!player.isMain && isRoster">
              (alternate)
            </span>
          </span>
          <span v-if="Number(playtime) > 0">
            {{ playtime }} hours
          </span>
        </div>
      </span>
    </div>
    <div v-else class="role-info">
      <span>
        {{ rosterStore.roleNames[roleTitle] }}
      </span>
    </div>
  </button>
</template>

<style scoped>
.player-card {
  background-color: var(--base-0);
  padding: 1em;
  border-radius: 8px;
  user-select: none;
  display: flex;
  gap: 1em;
  align-items: center;
  border: 2px solid var(--surface-0);
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
  flex-grow: 1;
}

.role-info .subtitle {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.player-card:hover {
  background-color: var(--surface-0);
  transition-duration: 200ms;
  border-color: var(--surface-0);
}

.player-card.no-player {
  border: 2px dashed var(--overlay-0);
  box-shadow: none;
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

.player-name {
  font-size: 16px;
  font-weight: 600;
}
</style>
