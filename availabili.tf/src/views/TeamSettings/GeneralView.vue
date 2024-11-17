<script setup lang="ts">
import { useTeamSettings } from '@/composables/team-settings';
import timezones from "@/assets/timezones.json";

const {
  teamName,
  timezone,
  minuteOffset,
} = useTeamSettings();
</script>

<template>
  <div class="team-general-settings">
    <div>
      <div class="form-group margin">
        <h3 class="closer">Team Name</h3>
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
            <v-select :options="timezones" v-model="timezone" />
          </div>
          <div class="form-group" id="minute-offset-group">
            <h3>Minute Offset</h3>
            <input type="number" v-model="minuteOffset" min="0" max="59" />
          </div>
        </div>
        <em class="aside">
          Matches will be scheduled based on {{ timezone }} at
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
        <div class="action-buttons">
          <button class="accent" @click="updateTeamSettings">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>
