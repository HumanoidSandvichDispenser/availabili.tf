<script setup lang="ts">
import { useAuthStore } from "../stores/auth";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const queryParams = computed(() => route.query);

const auth = useAuthStore();

const registerUsername = ref("");

function register() {
  //const params = {
  //  ...queryParams.value,
  //  username: registerUsername.value,
  //};

  //auth.login(params)
  //  .then(() => router.push("/"));
  auth.setUsername(registerUsername.value)
    .then(() => router.push("/"));
}

onMounted(() => {
  auth.login(queryParams.value)
    .then(() => {
      if (!auth.isRegistering) {
        router.push("/");
      }
    });
});
</script>

<template>
  <main>
    <div class="login-container">
      <template v-if="auth.isRegistering">
        <h1>New account</h1>
        <p>
          Your account has been newly created. Select a username to be
          associated with this account.
        </p>
        <div class="form-group margin">
          <h3>Username</h3>
          <input v-model="registerUsername" />
        </div>
        <div class="form-group margin">
          <div class="action-buttons">
            <button class="accent" type="submit" @click="register()">
              Save
            </button>
          </div>
        </div>
      </template>
      <div v-else>
        Logging in...
      </div>
    </div>
  </main>
</template>

<style scoped>
.login-container {
  align-items: center;
  max-width: 500px;
  margin: auto;
}

h3 {
  font-size: 11pt;
  font-weight: 700;
}
</style>
