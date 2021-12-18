<template>
  <Layout>
    <h1>Hello, Django! This is Gatsby!</h1>
    <p>
      Learning VueJS by using Gridsome to explore the Python Django library, as
      processed by Parso.
    </p>
    <p>I gotta be me, I guess.</p>
    <h2>Django Modules</h2>
    <ModuleSummary
      v-for="edge in $page.modules.edges"
      v-bind:key="edge.node.id"
      v-bind:module="edge.node"
    />
  </Layout>
</template>

<script>
import ModuleSummary from "~/components/ModuleSummary.vue";

export default {
  metaInfo: {
    title: "Hello, world!",
  },
  components: {
    ModuleSummary,
  },
};
</script>

<style>
.home-links a {
  margin-right: 1rem;
}
</style>

<page-query>
query {
  modules: allDjangoModule(sortBy: "module", order: ASC) {
    edges {
      node {
        id
        module
        docstring
      }
    }
  }
}
</page-query>