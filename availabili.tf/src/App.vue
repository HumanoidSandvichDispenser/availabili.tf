<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { useAuthStore } from "./stores/auth";
import ProfileDropdown from "./components/ProfileDropdown.vue";

const baseUrl = window.location.origin;

const authStore = useAuthStore();
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <h1>
          <RouterLink class="header-link" to="/">availabili.tf</RouterLink>
        </h1>
        <div class="nav-links">
          <a
            class="button"
            href="https://github.com/HumanoidSandvichDispenser/availabili.tf"
            v-tooltip="'View on GitHub'"
          >
            <button class="icon">
              <i class="bi bi-github" />
            </button>
          </a>
          <ProfileDropdown v-if="authStore.isLoggedIn" />
          <!--button v-if="authStore.isLoggedIn" class="profile-button">
            Welcome {{ authStore.username }}
          </button-->
          <form
            v-else
            action="https://steamcommunity.com/openid/login"
            method="get"
          >
            <input type="hidden" name="openid.identity"
                   value="http://specs.openid.net/auth/2.0/identifier_select" />
            <input type="hidden" name="openid.claimed_id"
                   value="http://specs.openid.net/auth/2.0/identifier_select" />
            <input type="hidden" name="openid.ns" value="http://specs.openid.net/auth/2.0" />
            <input type="hidden" name="openid.mode" value="checkid_setup" />
            <input type="hidden" name="openid.return_to" :value="baseUrl + '/login'" />
            <!--button type="submit">Log in through Steam</button-->
            <button type="submit" class="sign-in-button">
              <img src="https://community.fastly.steamstatic.com/public/images/signinthroughsteam/sits_01.png" />
            </button>
          </form>
        </div>
      </nav>
    </div>
  </header>

  <div class="content">
    <RouterView />
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

a.header-link {
  font-weight: 800;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  display: flex;
  width: 100%;
  text-align: center;
  margin: 0;
  align-items: center;
  justify-content: space-between;
}

nav .nav-links {
  display: flex;
  justify-content: end;
  align-items: center;
  font-size: 11pt;
  gap: 1rem;
}

button.profile-button {
  background-color: transparent;
}

nav a.router-link-exact-active {
  color: var(--text);
}

nav a {
  color: var(--subtext-0);
  border-radius: 8px;
}

nav a:hover {
  background-color: transparent;
}

nav > h1 {
  line-height: unset;
  margin-right: 1rem;
}

button.sign-in-button {
  background-color: transparent;
  border: none;
  padding: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
    width: 100%;
  }

  nav {
    text-align: left;
    font-size: 1rem;

    padding: 1rem 0;
  }
}

#app > div.content {
  display: flex;
}

#app > div.content > main {
  width: 100%;
}
</style>
