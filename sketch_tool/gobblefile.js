var gobble = require( 'gobble' );

module.exports = gobble([
  gobble('styles')
    .transform('sass', {
      src: 'main.scss',
      dest: 'main.css'
    }),

  gobble('lib')
    .transform('babel', {
      "optional": ["runtime"]
    })
    .moveTo('lib'),

  gobble('config.js'),
  gobble('jspm_packages').moveTo('jspm_packages'),

  gobble('html')
    .transform('replace', {
      systemjs_path: 'jspm_packages/system.js',
      configjs_path: 'config.js',
      css_path: 'main.css'
    })
]);
