const isDev = process.env.NODE_ENV === 'development'

module.exports = {
    webpackDevMiddleware: (config) => {
        config.watchOptions = {
            poll: 1000,
            aggregateTimeout: 300,
        };
        return config;
    },
    env: {
        backendHost: isDev ? "http://0.0.0.0:8000" : "https://dinner-me-backend.herokuapp.com",
    },
};
