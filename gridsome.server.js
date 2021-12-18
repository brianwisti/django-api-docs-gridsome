const fs = require('fs');
const path = require('path');

// Server API makes it possible to hook into various parts of Gridsome
// on server-side and add custom data to the GraphQL data layer.
// Learn more: https://gridsome.org/docs/server-api/

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

module.exports = function (api) {
  api.loadSource(({ addSchemaTypes }) => {
    addSchemaTypes(`
    type DjangoModule implements Node {
      id: ID!
      path: String
      module: String
      docstring: String
    }
    `)
  });

  api.loadSource(({ addCollection }) => {
    const moduleDir = './src/data/module'
    // Use the Data Store API here: https://gridsome.org/docs/data-store-api/
    const collection = addCollection({
      typeName: 'DjangoModule'
    })

    fs.readdir(moduleDir, (err, files) => {
      if (err) {
        throw err;
      }

      files.forEach(file => {
        const filePath = path.join(moduleDir, file);

        fs.readFile(filePath, 'utf-8', (err, data) => {
          if (err) {
            throw err;
          }

          const djangoModule = JSON.parse(data);
          // docstring
          // functions
          // - name
          // - params
          // - docstring
          // classes
          collection.addNode({
            path: file,
            module: path.basename(file, '.json'),
            docstring: djangoModule.docstring,
          });
        })
      })
    })
  })

  api.createPages(({ createPage }) => {
    // Use the Pages API here: https://gridsome.org/docs/pages-api/
  })
}
