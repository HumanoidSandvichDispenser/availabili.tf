<script setup lang="ts">
</script>

<template>
  <div class="match-card">
    <div class="match-scores">
      <div class="team-and-score">
        <span class="team-name">
          NVBLU
        </span>
        <span class="score">
          3
        </span>
      </div>
      <span class="score">-</span>
      <div class="team-and-score">
        <span class="score">
          2
        </span>
        <span class="team-name">
          RED
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.match-card {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  border: 1px solid var(--text);
  border-radius: 8px;
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
