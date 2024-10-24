<script setup lang="ts">
import PlayerCard from "../components/PlayerCard.vue";
import RoleSlot from "../components/RoleSlot.vue";
import PlayerTeamRole from "../player.ts";
import { reactive } from "vue";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const testPlayer: PlayerTeamRole = {
  name: "JustGetAHouse",
  role: "Pocket Scout",
  main: false,
}

const testPlayer2: PlayerTeamRole = {
  name: "Wesker U",
  role: "Pocket Scout",
  main: true,
}

const players = [testPlayer, testPlayer2];

const selectPlayers = reactive();
</script>

<template>
  <div class="columns">
    <div class="column">
      {{ rosterStore.selectedRole }}
      <PlayerCard :player="testPlayer" role-title="Pocket Scout" is-roster />
      <PlayerCard role-title="Flank Scout" is-roster />
      <PlayerCard role-title="Pocket Soldier" is-roster />
      <PlayerCard role-title="Roamer" is-roster />
      <PlayerCard role-title="Demoman" is-roster />
      <PlayerCard role-title="Medic" is-roster />
    </div>
    <div class="column">
    </div>
  </div>
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
}
</style>
