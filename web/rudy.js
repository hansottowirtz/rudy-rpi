document.addEventListener('DOMContentLoaded', function() {
  var command_input = document.getElementById('command');
  var command_button = document.getElementById('command-button');
  var speed = 100;

  command_button.addEventListener('click', function() {
    sendCommand(command_input.value);
  })

  var sendCommand = function(command) {
    var request = new Request('/api/command', {
      method: 'PUT',
      body: JSON.stringify({command: command}),
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    });
    fetch(request);
  }

  var park = function() {
    var request = new Request('/api/park', {
      method: 'PUT',
      body: 'null',
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    });
    fetch(request);
  }


  var execute = function(e, command) {
    e.preventDefault();
    sendCommand(command);
  }

  var up_button = document.getElementById('up');
  var down_button = document.getElementById('down');
  var right_button = document.getElementById('right');
  var left_button = document.getElementById('left');
  var center_button = document.getElementById('center');
  var pleft_button = document.getElementById('pleft');
  var pright_button = document.getElementById('pright');
  var brake_button = document.getElementById('brake');
  var plus_button = document.getElementById('speed-button-plus');
  var minus_button = document.getElementById('speed-button-minus');
  var speed_indicator = document.getElementById('speed-indicator');

  var us = function() {
    speed_indicator.innerHTML = speed;
  }

  up_button.addEventListener('mousedown', function(e){execute(e, 'M'+(500+speed));});
  up_button.addEventListener('mouseup', function(e){execute(e, 'M500');});
  down_button.addEventListener('mousedown', function(e){execute(e, 'M'+(500-speed));});
  down_button.addEventListener('mouseup', function(e){execute(e, 'M500');});
  left_button.addEventListener('click', function(e){execute(e, 'S000');});
  center_button.addEventListener('click', function(e){execute(e, 'S500');});
  right_button.addEventListener('click', function(e){execute(e, 'S999');});
  plus_button.addEventListener('click', function(e){speed += 50; speed = Math.min(400, speed); us();});
  minus_button.addEventListener('click', function(e){speed -= 50; speed = Math.max(100, speed); us();});
  pleft_button.addEventListener('click', function(e){park();});
  pright_button.addEventListener('click', function(e){park();});
});
