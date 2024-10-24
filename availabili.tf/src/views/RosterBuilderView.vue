<script setup lang="ts">
import PlayerCard from "../components/PlayerCard.vue";
import RoleSlot from "../components/RoleSlot.vue";
import PlayerTeamRole from "../player.ts";
import { computed, reactive } from "vue";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const hasAvailablePlayers = computed(() => {
  return rosterStore.availablePlayerRoles.length > 0;
});
</script>

<template>
  <main>
    <h1>Roster</h1>
    <div class="columns">
      <div class="column">
        <PlayerCard v-for="role in rosterStore.neededRoles"
                    :player="rosterStore.selectedPlayers[role]"
                    :role-title="role"
                    is-roster />
      </div>
      <div class="column">
        <h3 v-if="hasAvailablePlayers">Available</h3>
        <PlayerCard v-for="player in rosterStore.definitelyAvailable"
                    :player="player"
                    :role-title="player.role" />
        <span v-if="!hasAvailablePlayers">
          No players are currently available for this role.
        </span>
      </div>
      <div class="column">
        <h3 v-if="hasAvailablePlayers">Available if needed</h3>
        <PlayerCard v-for="player in rosterStore.canBeAvailable"
                    :player="player"
                    :role-title="player.role" />
      </div>
    </div>
  </main>
</template>

<style scoped>
.columns {
  display: flex;
  flex-direction: row;
}

.column {
  display: flex;
  flex-grow: 1;
  margin-left: 4em;
  margin-right: 4em;
  flex-direction: column;
  row-gap: 8px;
  width: 100%;
}

h3 {
  font-weight: 700;
  color: var(--subtext-0);
}
</style>
