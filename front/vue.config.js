const path = require('path');

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  outputDir: path.resolve(__dirname, '../back/dist'),
  assetsDir: 'static',
  publicPath: '/'
};