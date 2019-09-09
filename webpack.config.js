const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: [
        './pyblitzui/src/index.js'
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                  fallback: 'style-loader',
                  use: [
                    'css-loader',
                    'sass-loader'
                  ]
                })
              }
        ]
    },
    output: {
        path: __dirname + '/pyblitzui/static',
        filename: 'bundle.js'
    },
    plugins: [
      new ExtractTextPlugin('css/mystyles.css'),
    ]
};
