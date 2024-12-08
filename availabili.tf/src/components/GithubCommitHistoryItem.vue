<script setup lang="ts">
import type Commit from "@/commit";
import { computed } from "vue";

const props = defineProps<{
  commit: Commit;
}>();

const summary = computed(() => {
  return props.commit.commit.message.split("\n\n")[0];
});

const description = computed(() => {
  return props.commit.commit.message.split("\n\n")[1];
});
</script>

<template>
  <div class="commit-history-item">
    <div class="header">
      <span class="circle"></span>
      <a :href="commit.html_url">
        <h3>
          {{ summary }}
        </h3>
      </a>
    </div>
    <div class="description" v-if="description">
      {{ description }}
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
}

.header a {
  color: var(--text);
}

.circle {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--green);
  margin-right: 1em;
}

.description {
  padding: 0.5rem 2rem;
  color: var(--subtext-0);

}
</style>
