import "./assets/main.css";
import "vue-select/dist/vue-select.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import VueSelect from "vue-select";

import App from "./App.vue";
import router from "./router";

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component("v-select", VueSelect);

app.mount("#app")
