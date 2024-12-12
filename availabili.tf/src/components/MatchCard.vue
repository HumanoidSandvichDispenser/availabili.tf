<script setup lang="ts">
import type { TeamMatchSchema, TeamSchema } from '@/client';
import moment from 'moment';
import { computed } from 'vue';

const matchTime = computed(() => moment(props.teamMatch.match.matchTime)
  .format("LL LT"));

const props = defineProps<{
  team: TeamSchema,
  teamMatch: TeamMatchSchema,
}>();
</script>

<template>
  <div class="match-card">
    <div class="match-title">
      <h3>
        {{ teamMatch.match.logsTfTitle }}
      </h3>
    </div>
    <div class="match-scores">
      <div class="team-and-score">
        <span class="team-name">
          <span v-if="teamMatch.teamColor == 'Blue'">
            BLU
          </span>
          <span v-else>
            RED
          </span>
        </span>
        <span class="score">
          {{ teamMatch.ourScore }}
        </span>
      </div>
      <div class="team-and-score">
        <span class="score">
          {{ teamMatch.theirScore }}
        </span>
        <span class="team-name">
          <span v-if="teamMatch.teamColor == 'Blue'">
            RED
          </span>
          <span v-else>
            BLU
          </span>
        </span>
      </div>
    </div>
    <div class="bottom-row">
      <div class="subtext">
        {{ matchTime }}
      </div>
      <div>
        <a :href="'https://logs.tf/' + teamMatch.match.logsTfId" target="_blank" class="button">
          #{{ teamMatch.match.logsTfId }}
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.match-card {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border: 1px solid var(--text);
  border-radius: 8px;
  gap: 0.5rem;
}

.match-title {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.bottom-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom-row > div {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.match-scores {
  display: flex;
  justify-content: space-evenly;
  width: 100%;
  font-weight: 700;
}

.match-scores span {
  font-weight: 700;
}

.team-and-score {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.match-scores .score {
  font-size: 1.5rem;
}
</style>
