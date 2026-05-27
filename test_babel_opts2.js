const register = require('@babel/register');
const path = require('path');
const debugPath = path.resolve('node_modules/debug/src/index.js');

// Monkey-patch the worker to see what options are used
const workerClient = require('@babel/register/lib/worker-client.cjs');
const original = workerClient.Client.prototype.transform;
workerClient.Client.prototype.transform = function(code, filename) {
  console.log('Transform called for:', filename);
  return original.call(this, code, filename);
};

require('@babel/register');

(async () => {
  const mod = await import('debug');
  console.log('type:', typeof mod.default);
})();
