console.log 'Qikify View Server'

io   = require('socket.io').listen(8001)
fs   = require('fs')                                                                     
http = require('http')

zmq  = require('zmq')
sock = zmq.socket('sub')

sock.connect('tcp://127.0.0.1:3000');
console.log('Worker connected to port 3000');

io.sockets.on('connection', (socket) ->
    socket.emit('message', 'Connected to web socket server.')    
    socket.on('message', (msg) -> console.log('*** Message received from client: ' + msg))
    
)





