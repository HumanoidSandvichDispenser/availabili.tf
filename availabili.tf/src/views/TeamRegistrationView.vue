<script lang="ts" setup>
import { ref, watch } from "vue";
import { useTeamsStore } from "../stores/teams";
//import timezones from "../assets/timezones.json";
import { useRouter } from "vue-router";
import ComboBox from "../components/ComboBox.vue";
import { getTimeZones, type TimeZone } from "@vvo/tzdb";
import moment from "moment";

const timezones = getTimeZones({

});

console.log(timezones.length);

console.log(moment.tz.names());

const teams = useTeamsStore();

const router = useRouter();

const teamName = ref("");

const timezone = ref<TimeZone>(timezones.find((tz) => tz.name === "America/New_York")!);

const timezoneStr = ref("");

const minuteOffset = ref(0);

watch(minuteOffset, (newValue) => {
  minuteOffset.value = Math.min(Math.max(0, newValue), 59);
});

function createTeam() {
  teams.createTeam(teamName.value, timezone.value.name, minuteOffset.value)
    .then(() => {
      router.push("/");
    });
}
</script>

<template>
  <main>
    <div class="team-registration-container">
      <h1>Create a new team</h1>
      <p>
        Register your team to streamline match scheduling, role assignments,
        and overall team communication.
      </p>
      <div class="form-group margin">
        <h3>Team Name</h3>
        <input v-model="teamName" />
      </div>
      <div class="form-group margin">
        <div class="form-group row">
          <div class="form-group">
            <h3>
              Timezone
              <a
                class="aside"
                href="https://nodatime.org/TimeZones"
                target="_blank"
              >
                (view all timezones)
              </a>
            </h3>
            <v-select :options="timezones" label="name" v-model="timezone" />
          </div>
          <div class="form-group" id="minute-offset-group">
            <h3>Minute Offset</h3>
            <input type="number" v-model="minuteOffset" min="0" max="59" />
          </div>
        </div>
        <em class="aside">
          Matches will be scheduled based on {{ timezone.alternativeName }} at
          {{ minuteOffset }}
          <span v-if="minuteOffset == 1">
            minute
          </span>
          <span v-else>
            minutes
          </span>
          past the hour.
        </em>
      </div>
      <div class="form-group margin">
        <div class="banner info">
          <i class="bi bi-info-circle" />
          Note: changing the timezone or minute offset after team creation
          will remove all team members' availability data.
        </div>
      </div>
      <div class="form-group margin">
        <div class="action-buttons">
          <button class="accent" @click="createTeam">Create team</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.team-registration-container {
  align-items: center;
  max-width: 500px;
  margin: auto;
}

.team-registration-container .aside {
  font-size: 9pt;
}

#minute-offset-group {
  flex-grow: unset;
  flex-shrink: 1;
  flex-basis: 25%;
}

input {
  display: block;
  width: 100%;
  color: var(--text);
}
</style>
