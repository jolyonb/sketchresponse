module.exports = function(config) {
  config.set({
    autoWatch: true,
    frameworks: ['jspm', 'jasmine', 'phantomjs-shim'],
    browsers: ['PhantomJS'],
    jspm: {
      loadFiles: [
        'test/**/*.js',
      ],
      serveFiles: ['lib/**/*.js']
    }
  });
};
