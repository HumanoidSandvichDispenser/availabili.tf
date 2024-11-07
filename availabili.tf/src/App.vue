<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";

const baseUrl = window.location.origin;
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <h1>availabili.tf</h1>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/schedule">Schedule</RouterLink>
        <RouterLink to="/schedule/roster">Roster Builder</RouterLink>
        <form action="https://steamcommunity.com/openid/login" method="get">
          <input type="hidden" name="openid.identity"
                 value="http://specs.openid.net/auth/2.0/identifier_select" />
          <input type="hidden" name="openid.claimed_id"
                 value="http://specs.openid.net/auth/2.0/identifier_select" />
          <input type="hidden" name="openid.ns" value="http://specs.openid.net/auth/2.0" />
          <input type="hidden" name="openid.mode" value="checkid_setup" />
          <input type="hidden" name="openid.return_to" :value="baseUrl + '/login'" />
          <button type="submit">Log in through Steam</button>
        </form>
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

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  display: flex;
  gap: 8px;
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin: 0;
  align-items: center;
}

nav a.router-link-exact-active {
  color: var(--crust);
  background-color: var(--accent);
}

nav a {
  padding: 0.5rem 1rem;
  color: var(--subtext-0);
  border-radius: 8px;
}

nav a:hover {
  color: var(--accent);
  background-color: var(--accent-transparent);
}

nav > h1 {
  line-height: unset;
  margin-right: 1rem;
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
    margin-left: -1rem;
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
