document.addEventListener('DOMContentLoaded', function(){
  var command_input = document.getElementsByName('command')[0];
  var command_button = document.getElementsByName('command-button')[0];
  command_button.addEventListener('click', function(){
    var request = new Request('/api/command', {
      method: 'PUT',
      body: JSON.stringify({command: command_input.value}),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    });
    fetch(request);
  })
});
