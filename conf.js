'use strict';

// protractor configuration

exports.config = {
  //seleniumAddress: 'http://localhost:4444/wd/hub',
  specs: ['purkinje/static/js/tests/e2e/*.spec.js'],

  capabilities: {
    browserName: 'firefox'
  }
};
