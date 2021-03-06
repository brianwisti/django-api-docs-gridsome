// This is where project configuration and plugin options are located.
// Learn more: https://gridsome.org/docs/config

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

module.exports = {
  siteName: 'Django API Docs',
  plugins: [],
  templates: {
    DjangoModule: [
      {
        path: '/module/:module',
        component: './src/templates/DjangoModule.vue',
      },
    ]
  }
}
