<script setup lang="ts">
import { useTeamsStore } from "../stores/teams";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { computed } from "vue";
import { useTeamDetails } from "../composables/team-details";
import PlayerTeamCard from "../components/PlayerTeamCard.vue";
import InviteEntry from "../components/InviteEntry.vue";

const route = useRoute();
const router = useRouter();
const teamsStore = useTeamsStore();
const {
  team,
  invites,
  availableMembers,
  availableMembersNextHour,
  teamMembers,
} = useTeamDetails();

function createInvite() {
  teamsStore.createInvite(team.value.id);
}

function leaveTeam() {
  teamsStore.leaveTeam(team.value.id)
    .then(() => {
      teamsStore.fetchTeams()
        .then(() => {
          router.push("/");
        })
    });
}
</script>

<template>
  <div class="member-list-header">
    <h2>Members</h2>
    <em class="aside" v-if="teamMembers">
      {{ teamMembers?.length }} member(s),
      {{ availableMembers?.length }} currently available,
      {{ availableMembersNextHour?.length }} available in the next hour
    </em>
    <div class="team-details-button-group">
      <RouterLink class="button" :to="'/schedule?teamId=' + team.id">
        <button class="accent">
          <i class="bi bi-calendar-fill margin"></i>
          View schedule
        </button>
      </RouterLink>
      <button
        class="destructive"
        @click="leaveTeam"
      >
        Leave
      </button>
    </div>
  </div>
  <table class="member-table">
    <tbody>
      <PlayerTeamCard
        v-for="member in teamMembers"
        :player="member"
        :team="team"
        :key="member.username"
      />
    </tbody>
  </table>
  <h2>Active Invites</h2>
  <div>
    <details>
      <summary>View all invites</summary>
      <span v-if="invites?.length == 0">
        There are currently no active invites to this team.
      </span>
      <table id="invite-table" v-else>
        <thead>
          <tr>
            <th>
              Key (hover to reveal)
            </th>
            <th>
              Creation time
            </th>
          </tr>
        </thead>
        <tbody>
          <InviteEntry
            v-for="invite in invites"
            :invite="invite"
          />
        </tbody>
      </table>
      <div class="create-invite-group">
        <button class="accent" @click="createInvite">
          <i class="bi bi-person-fill-add margin" />
          Create Invite
        </button>
        <span class="small aside">
          Invites are usable once and expire after 24 hours.
        </span>
      </div>
    </details>
  </div>
</template>

<style scoped>
.member-list-header {
  display: flex;
  gap: 0.5em;
  align-items: center;
}

.member-list-header > .aside {
  font-size: 12pt;
  font-style: normal;
}

table.member-table {
  width: 100%;
}

table.member-table th {
  text-align: left;
  padding-left: 2em;
  font-weight: 700;
}

th {
  text-align: left;
  font-weight: 600;
  padding: 8px;
}

#invite-table {
  width: 100%;
  border: 1px solid var(--text);
  margin: 8px 0;
}

.team-details-button-group {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: end;
  gap: 4px;
}

.create-invite-group {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
