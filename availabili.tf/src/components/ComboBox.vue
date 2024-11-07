<script setup lang="ts">
import { computed, defineModel, defineProps, ref } from "vue";

const model = defineModel();

const props = defineProps({
  options: Array<String>,
  isDisabled: Boolean,
});

const isOpen = ref(false);
const selectedOption = computed(() => props.options[model.value]);

function selectOption(index) {
  model.value = index;
  isOpen.value = false;
}
</script>

<template>
  <div :class="{ 'dropdown-container': true, 'is-open': isOpen }">
    <button @click="isOpen = !isOpen" :disabled="isDisabled">
      {{ selectedOption }}
      <i class="bi bi-caret-down-fill"></i>
    </button>
    <ul class="dropdown" v-if="isOpen" @blur="isOpen = false">
      <li v-for="(option, i) in options" :key="i" @click="selectOption(i)">
        <button :class="{ 'is-selected': i == model }">
          {{ option }}
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.dropdown-container {
  display: inline-block;
  border-radius: 8px;
}

.dropdown-container button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  text-align: left;
  font-weight: 700;
  font-size: 16px;
  padding: 4px;
  transition-duration: 200ms;
  background-color: transparent;
  cursor: pointer;
}

.dropdown-container button:hover {
  background-color: var(--crust);
}

.dropdown-container.is-open ul.dropdown {
  box-shadow: 1px 1px 8px var(--shadow);
}

ul.dropdown {
  display: block;
  background-color: var(--base);
  position: absolute;
  margin-top: 8px;
  padding: 0;
  z-index: 2;
  border-radius: 8px;
  overflow: none;
}

ul.dropdown > li {
  list-style-type: none;
}

.dropdown li > button {
  padding: 8px 16px;
  font-weight: 500;
  font-size: 14px;
  border-radius: 0;
}

.dropdown li > button.is-selected {
  background-color: var(--accent-transparent);
  color: var(--accent);
}
</style>
