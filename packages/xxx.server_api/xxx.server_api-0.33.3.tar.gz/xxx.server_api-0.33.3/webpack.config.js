var webpack = require('webpack');
module.exports = {
    context: __dirname + '/xxx/server_api/static',
    entry: './angular_source/app.js',
    output: {
        path: __dirname + '/xxx/server_api/static',
        filename: 'bundle.js'
    },
    plugins: [
        new webpack.ProvidePlugin({
            '$': 'jquery',
            'window.jQuery': 'jquery',
            'jQuery': 'jquery',
            'window.$': 'jquery'
        })
],
};