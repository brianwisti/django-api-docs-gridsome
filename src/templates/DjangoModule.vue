<template>
  <Layout>
    <h1 v-html="$page.module.module" />
    <pre
      v-if="$page.module.docstring"
      v-html="$page.module.docstring"
      class="docstring"
    />
  </Layout>
</template>

<page-query>
query ($id: ID!) {
    module: djangoModule(id: $id) {
        module
        docstring
    }
}
</page-query>