<script setup lang="ts">
import { useRoute, useRouter, RouterLink, RouterView } from "vue-router";
import { useTeamsStore } from "@/stores/teams";
import { useInvitesStore } from "@/stores/teams/invites";
import { computed, onMounted, ref } from "vue";
import { useTeamDetails } from "@/composables/team-details";
import MembersList from "@/components/MembersList.vue";
import moment from "moment";
import EventList from "@/components/EventList.vue";
import { useTeamsEventsStore } from "@/stores/teams/events";
import MatchCard from "@/components/MatchCard.vue";
import { useMatchesStore } from "@/stores/matches";
import { ContentLoader } from "vue-content-loader";

const route = useRoute();
const teamsStore = useTeamsStore();
const invitesStore = useInvitesStore();
const matchesStore = useMatchesStore();
const { team, teamId } = useTeamDetails();

const creationDate = computed(() => {
  if (team.value) {
    return moment(team.value.createdAt).format("L");
  }
});

const key = computed(() => route.query.key);

const teamsEventsStore = useTeamsEventsStore();
const events = computed(() => teamsEventsStore.teamEvents[teamId.value]);
const matches = computed(() => matchesStore.recentMatches);
const isLoading = ref(false);

onMounted(() => {
  isLoading.value = true;
  let doFetchTeam = () => {
    teamsStore.fetchTeam(teamId.value)
      .then(() => {
        teamsStore.fetchTeamMembers(teamId.value);
        teamsEventsStore.fetchTeamEvents(teamId.value);
        matchesStore.fetchRecentMatchesForTeam(teamId.value, 5);
        isLoading.value = false;
      });
  };

  if (key.value) {
    invitesStore.consumeInvite(key.value.toString())
      .finally(doFetchTeam);
  } else {
    doFetchTeam();
  }
});
</script>

<template>
  <main>
    <template v-if="team">
      <div class="content-container">
        <div class="left">
          <center class="margin">
            <h1>
              <template v-if="isLoading || true">
                <content-loader view-box="0 0 250 10">
                  <rect x="0" y="0" rx="3" ry="3" width="250" height="10" />
                </content-loader>
              </template>
              <template v-else>
                {{ team.teamName }}
              </template>
            </h1>
            <span class="aside">
              Formed on {{ creationDate }}
            </span>
            <div class="icons">
              <RouterLink class="button" :to="'/schedule?teamId=' + team.id">
                <button class="icon" v-tooltip="'Schedule'">
                  <i class="bi bi-calendar-fill"></i>
                </button>
              </RouterLink>
              <RouterLink class="button" :to="{ name: 'team-settings/' }">
                <button class="icon" v-tooltip="'Settings'">
                  <i class="bi bi-gear-fill"></i>
                </button>
              </RouterLink>
            </div>
          </center>
          <MembersList />
        </div>
        <div class="right">
          <h2>Upcoming Events</h2>
          <EventList :events="events" :team-context="team" />
          <h2 id="recent-matches-header">
            Recent Matches
            <RouterLink class="button" :to="{ name: 'team-settings/matches' }">
              <button class="icon" v-tooltip="'View all'">
                <i class="bi bi-arrow-right-circle-fill"></i>
              </button>
            </RouterLink>
          </h2>
          <em class="subtext" v-if="!matches">
            No recent matches.
          </em>
          <MatchCard
            v-else
            v-for="match in matches"
            :team-match="match"
            :team="team"
          />
        </div>
      </div>
    </template>
  </main>
</template>

<style scoped>
#recent-matches-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-container {
  display: flex;
  justify-content: space-between;
}

.content-container > div.left {
  flex: 2;
}

.content-container > div.right {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-top: 4em;
  gap: 1rem;
}

.margin {
  margin: 4em;
}

.icons {
  display: flex;
  justify-content: center;
  margin: 8px;
  gap: 4px;
}

.icons a {
  border-radius: 4px;
}

.icons button {
  color: var(--overlay-0);
  font-size: 12pt;
}

.icons button:hover {
  color: var(--text);
}

@media (max-width: 1024px) {
  .content-container {
    flex-direction: column;
  }
}
</style>
