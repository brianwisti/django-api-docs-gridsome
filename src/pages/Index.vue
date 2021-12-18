<template>
  <Layout>
    <!-- Learn how to use images here: https://gridsome.org/docs/images -->
    <g-image alt="Example image" src="~/favicon.png" width="135" />

    <h1>Hello, world!</h1>
    <p>
      Learning VueJS by using Gridsome to explore the Python Django library, as
      processed by Parso.
    </p>
    <p>I gotta be me, I guess.</p>
    <h2>Django Modules</h2>
    <div v-for="edge in $page.modules.edges" :key="edge.node.id">
      <h3>{{ edge.node.module }}</h3>
      <pre>{{ edge.node.docstring }}</pre>
    </div>
  </Layout>
</template>

<script>
export default {
  metaInfo: {
    title: "Hello, world!",
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