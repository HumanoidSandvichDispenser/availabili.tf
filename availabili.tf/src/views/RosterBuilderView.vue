<script setup lang="ts">
import PlayerCard from "../components/PlayerCard.vue";
import RoleSlot from "../components/RoleSlot.vue";
import PlayerTeamRole from "../player.ts";
import { computed, reactive, onMounted } from "vue";
import { useRosterStore } from "../stores/roster";
import { useRoute } from "vue-router";
import moment from "moment";

const rosterStore = useRosterStore();

const route = useRoute();

const hasAvailablePlayers = computed(() => {
  return rosterStore.availablePlayerRoles.length > 0;
});

const hasAlternates = computed(() => {
  return rosterStore.alternateRoles.length > 0;
});

onMounted(() => {
  rosterStore.fetchAvailablePlayers(route.params.startTime, route.params.teamId);
});
</script>

<template>
  <main>
    <div class="top">
      <h1 class="roster-title">
        Roster for Snus Brotherhood
        <em class="aside date">
          @
          {{ moment(startTime).format("L LT") }}
        </em>
      </h1>
      <div class="button-group">
        <button>Cancel</button>
        <button class="accent">Save Roster</button>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <PlayerCard v-for="role in rosterStore.neededRoles"
                    :player="rosterStore.selectedPlayers[role]"
                    :role-title="role"
                    is-roster />
      </div>
      <div class="column">
        <PlayerCard v-for="player in rosterStore.mainRoles"
                    :player="player"
                    :role-title="player.role" />
        <span v-if="!hasAvailablePlayers && rosterStore.selectedRole">
          No players are currently available for this role.
        </span>
        <h3 v-if="hasAvailablePlayers">Alternates</h3>
        <PlayerCard v-for="player in rosterStore.alternateRoles"
                    :player="player"
                    :role-title="player.role" />
        <PlayerCard v-if="rosterStore.selectedRole"
                    is-ringer
                    :role-title="rosterStore.selectedRole" />
      </div>
    </div>
  </main>
</template>

<style scoped>
.top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.top .button-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

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

.column h3 {
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  color: var(--overlay-0);
}

.roster-title {
  display: flex;
  gap: 0.5em;
}

em.aside.date {
  font-size: 14px;
  vertical-align: middle;
}
</style>
