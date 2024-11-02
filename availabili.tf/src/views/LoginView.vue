<script setup lang="ts">
import { useAuthStore } from "../stores/auth";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const queryParams = route.query;

const auth = useAuthStore();

const registerUsername = ref("");

function register() {
  const params = {
    ...queryParams,
    username: registerUsername,
  }

  auth.login(params)
    .then(() => router.push("/"));
}

onMounted(() => {
  if (Object.keys(queryParams).length == 0) {
    auth.isRegistering = true;
    return;
  }

  auth.login(queryParams)
    .then(() => router.push("/"));
});
</script>

<template>
  <div>
    <main>
      <template v-if="auth.isRegistering">
        <h1>Register</h1>
        <input v-model="registerUsername" />
        <button class="accent" type="submit">Register</button>
      </template>
      <div v-else>
        Logging in...
      </div>
    </main>
  </div>
</template>
