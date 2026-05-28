require('@babel/runtime');
(async () => {
  const mod = await import('debug');
  console.log('type:', typeof mod.default);
})();
