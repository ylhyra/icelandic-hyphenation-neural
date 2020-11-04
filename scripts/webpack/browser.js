const path = require('path')
const webpack = require('webpack');
const resolve = (input) => path.resolve(__dirname, './../../' + input)
// const NodemonPlugin = require('nodemon-webpack-plugin')

// const polyfills = resolve('scripts/webpack/utils/config/polyfills.js')
const modules = [
  resolve('.'),
  resolve('website'),
  resolve('node_modules'),
]

module.exports = {
  // target: 'node',
  node: {
    __dirname: true,
    __filename: false,
  },
  mode: process.env.NODE_ENV,
  entry: {
    core: [ /*polyfills,*/ resolve('core/index.js')],
    website: [ /*polyfills,*/ resolve('website/frontend/index.js')],
    // server: [ /*polyfills,*/ resolve('website/server/index.js')],
  },
  output: {
    path: resolve('build/js'),
    filename: '[name].js'
  },
  resolve: {
    modules: modules,
    extensions: ['.js'],
  },
  devtool: process.env.NODE_ENV === 'development' ? 'source-map' : false,
  watchOptions: {
    ignored: ['node_modules/**', 'build/**']
  },

  // this should go into the webpack.dev.js
  devServer: {
    //contentBase: path.join(__dirname, "/dist"),
    compress: true,
    port: 3100,
    hot: true,
    stats: "errors-only",
    open: true
  },

  module: {
    strictExportPresence: true,
    rules: [{
      oneOf: [{
        test: /\.(js)$/,
        include: modules,
        loader: require.resolve('babel-loader'),
        options: {
          cacheDirectory: true,
        },
      }, ],
    }, ],
  },
  // optimization: {
  //   splitChunks: {
  //     cacheGroups: {
  //       commons: {
  //         // this takes care of all the vendors in your files
  //         // no need to add as an entrypoint.
  //         test: /[\\/]node_modules[\\/]/,
  //         name: 'vendors',
  //         chunks: 'all'
  //       }
  //     }
  //   }
  // },
}
