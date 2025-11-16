window.addEventListener('load', () => {
  // Check if navigation type is back_forward (2)
  if (performance.getEntriesByType("navigation")[0].type === 'back_forward') {
    console.log('Back or forward navigation detected - reloading');
    window.location.reload();
  }
  else{
    console.log("not reloading");
  }
});

