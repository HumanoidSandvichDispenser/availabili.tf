<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { onMounted, ref } from "vue";

const displayName = ref("");

const authStore = useAuthStore();

function save() {
  authStore.setUsername(displayName.value);
}

onMounted(() => {
  displayName.value = authStore.username;
});
</script>

<template>
  <main>
    <div class="user-settings-container">
      <h1>User Settings</h1>
      <div class="form-group margin">
        <h3>
          Display Name
        </h3>
        <input v-model="displayName" />
      </div>
      <div class="form-group margin">
        <div class="action-buttons">
          <button class="accent" @click="save">Save</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.user-settings-container {
  align-items: center;
  max-width: 500px;
  margin: auto;
}
</style>
