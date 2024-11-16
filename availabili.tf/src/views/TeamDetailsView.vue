<script setup lang="ts">
import { useRoute, useRouter, RouterLink } from "vue-router";
import { useTeamsStore } from "../stores/teams";
import { computed, onMounted, ref } from "vue";
import PlayerTeamCard from "../components/PlayerTeamCard.vue";
import InviteEntry from "../components/InviteEntry.vue";
import moment from "moment";

const route = useRoute();
const router = useRouter();
const teamsStore = useTeamsStore();

const team = computed(() => {
  return teamsStore.teams[route.params.id];
});

const creationDate = computed(() => {
  if (team.value) {
    return moment(team.value.createdAt).format("L");
  }
});

const invites = computed(() => {
  return teamsStore.teamInvites[route.params.id];
});

const availableMembers = computed(() => {
  return teamsStore.teamMembers[route.params.id]
    .filter((member) => member.availability[0] > 0);
});

const availableMembersNextHour = computed(() => {
  return teamsStore.teamMembers[route.params.id]
    .filter((member) => member.availability[1] > 0);
});

function createInvite() {
  teamsStore.createInvite(team.value.id);
}

function revokeInvite(key) {
  teamsStore.revokeInvite(team.value.id, key)
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

onMounted(async () => {
  let key = route.query.key;
  let teamId = route.params.id;

  let doFetchTeam = () => {
    teamsStore.fetchTeam(teamId)
      .then(() => teamsStore.fetchTeamMembers(teamId))
      .then(() => teamsStore.getInvites(teamId));
  };

  if (key) {
    teamsStore.consumeInvite(teamId, key)
      .finally(doFetchTeam);
  } else {
    doFetchTeam();
  }

});
</script>

<template>
  <main>
    <template v-if="team">
      <center class="team-info">
        <h1>
          {{ team.teamName }}
        </h1>
        <span class="aside">
          Formed on {{ creationDate }}
        </span>
      </center>
      <div class="member-list-header">
        <h2>Members</h2>
        <em class="aside" v-if="teamsStore.teamMembers[route.params.id]">
          {{ teamsStore.teamMembers[route.params.id]?.length }} member(s),
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
        <!--thead>
          <tr>
            <th>
              Name
            </th>
            <th>
              Roles
            </th>
            <th>
              Playtime on team
            </th>
            <th>
              Joined
            </th>
          </tr>
        </thead-->
        <tbody>
          <PlayerTeamCard
            v-for="member in teamsStore.teamMembers[route.params.id]"
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
  </main>
</template>

<style scoped>
.team-info {
  margin: 4em;
}

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

/*
div.member-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
*/

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
