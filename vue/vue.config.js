const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
// const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');

const isLocal = process.env.VUE_APP_MODE === 'local'
const publicPath = process.env.VUE_APP_PUBLIC
const statFile = process.env.VUE_APP_STAT_FILE

const statRoot = path.resolve(path.join(path.dirname(__dirname), 'stats'));
// const statFile = isProd ? 'webpack-stats-prod.json' : 'webpack-stats.json';
// const publicPath = isProd ? '/static/bundles/' : 'http://0.0.0.0:5050/';
const outputDir = path.resolve(path.join(path.dirname(statRoot), 'app/static/bundles'));


module.exports = {
    // pages: {
    //     app: 'src/main.js',
    // },
    // assetsDir: 'assets',
    outputDir: outputDir,
    publicPath: publicPath,
    runtimeCompiler: true,
    lintOnSave: false,
    productionSourceMap: false,
    css: {
        extract: true
    },
    chainWebpack: (config) => {
        // config.optimization.splitChunks(false);
        config.plugin('BundleTracker').use(BundleTracker, [{path: statRoot, filename: statFile}]);
        // new MonacoWebpackPlugin()

        // config.resolve.alias.set('__STATIC__', 'static');
        config.resolve.modules.add('./src');
        config.resolve.modules.add(path.join(__dirname, 'src/components'));

        if (isLocal) {
            config.devServer
                .public('http://0.0.0.0:5050')
                .host('0.0.0.0').port(5050)
                .hotOnly(true)
                .watchOptions({poll: 1000})
                .https(false)
                .headers({'Access-Control-Allow-Origin': ['*']})
        } else {
            config.optimization.minimize(true)
        }
    }
};
