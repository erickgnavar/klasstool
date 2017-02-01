console.log('Klasstool session stream started!');

var scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
var socket = new ReconnectingWebSocket(scheme + '://' + window.location.host + window.location.pathname);

socket.onmessage = function(e) {
  console.log('Message received: ' + e.data);
}

socket.onopen = function() {
  console.log('Socket connected!');
}

if (socket.readyState == WebSocket.OPEN) {
  socket.onopen();
}
