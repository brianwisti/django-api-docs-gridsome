const fs = require('fs');
const path = require('path');

// Server API makes it possible to hook into various parts of Gridsome
// on server-side and add custom data to the GraphQL data layer.
// Learn more: https://gridsome.org/docs/server-api/

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

module.exports = function (api) {
  api.loadSource(({ addSchemaTypes }) => {
    // library
    // package
    // module
    addSchemaTypes(`
      type PythonModule implements Node @infer {
        id: ID!
        namespace: String! @unique
      }

      type PythonPackage implements Node @infer {
        id: ID!
        name: String! @unique
        docstring: String
        subpackages: [PythonPackage]! @reference(by: "name")
        modules: [PythonModule]! @reference(by: "namespace")
      }

      type PythonLibrary implements Node {
        id: ID!
        packages: [PythonPackage]! @reference(by: "name")
      }
    `)
  });

  api.loadSource(({ addCollection, getCollection, }) => {
    // Use the Data Store API here: https://gridsome.org/docs/data-store-api/

    const moduleDir = './src/data/mod';
    const moduleCollection = addCollection('PythonModule');

    fs.readdir(moduleDir, (err, files) => {
      if (err) { throw err }

      files.forEach(file => {
        const filePath = path.join(moduleDir, file);

        fs.readFile(filePath, 'utf-8', (err, data) => {
          if (err) { throw err }

          const pythonModule = JSON.parse(data);
          moduleCollection.addNode(pythonModule);
        })
      })
    });

    const packageDir = './src/data/pkg';
    const packageCollection = addCollection('PythonPackage');

    fs.readdir(packageDir, (err, files) => {
      if (err) { throw err }

      files.forEach(file => {
        const filePath = path.join(packageDir, file);

        fs.readFile(filePath, 'utf-8', (err, data) => {
          if (err) { throw err }

          const pythonPackage = JSON.parse(data);
          packageCollection.addNode({ ...pythonPackage });
        })
      })
    });

    const libraryCollection = addCollection('PythonLibrary');
    const libraryPath = './src/data/library.json';
    fs.readFile(libraryPath, 'utf-8', (err, data) => {
      if (err) { throw err }

      const pythonLibrary = JSON.parse(data);
      console.log(pythonLibrary)
      libraryCollection.addNode(pythonLibrary);
    })
  })

  api.createPages(({ createPage }) => {
    // Use the Pages API here: https://gridsome.org/docs/pages-api/
  })
}
