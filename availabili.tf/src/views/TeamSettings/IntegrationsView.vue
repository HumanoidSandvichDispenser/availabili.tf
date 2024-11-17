<script setup lang="ts">
</script>

<template>
  <div class="team-integrations">
    <h2>Team Integrations</h2>
    <div v-if="true">
      This team currently does not have any integrations.
    </div>
    <div v-else>
      <details class="accordion">
        <summary>
          <h2>Discord Webhook</h2>
        </summary>
        <h3>Webhook URL</h3>
        <input hidden />
      </details>
    </div>
  </div>
</template>
