const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: [
        './src/index.js'
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
        path: __dirname + '/static',
        filename: 'bundle.js'
    },
    plugins: [
      new ExtractTextPlugin('css/mystyles.css'),
    ]
};


///
// const path = require('path');
// const ExtractTextPlugin = require("extract-text-webpack-plugin");

// module.exports = {
//   entry: './src/index.js',
//   output: {
//     path: path.resolve(__dirname, 'dist'),
//     filename: 'js/bundle.js'
//   },
//   module: {
//     rules: [{
//       test: /\.scss$/,
//       use: ExtractTextPlugin.extract({
//         fallback: 'style-loader',
//         use: [
//           'css-loader',
//           'sass-loader'
//         ]
//       })
//     }]
//   },
//   plugins: [
//     new ExtractTextPlugin('css/mystyles.css'),
//   ]
// };
