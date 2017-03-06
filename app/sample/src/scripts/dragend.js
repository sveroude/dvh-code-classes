document.addEventListener('DOMContentLoaded', function() {
  var component = document.querySelector('[data-dragend]');

  dragend = new Dragend(component, {
    afterInitialize: function() {
      component.style.visibility = 'visible';
    }
  });
}, false)
