<template>
  <div class="module-summary">
    <header>{{ module.module }}</header>
    <pre v-if="module.docstring" class="docstring">{{ module.docstring }}</pre>
  </div>
</template>

<script>
export default {
  props: ["module"],
};
</script>

<style scoped>
.module-summary {
  margin: 1rem;
}

.module-summary header {
  font-weight: bold;
  border: thin solid black;
}

.docstring {
  background-color: #ffffaa;
  padding: 0.5rem;
}
</style>
