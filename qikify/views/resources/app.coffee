io   = require('socket.io').listen(8001)
fs   = require('fs')                                                                     
http = require('http')
zmq  = require('zmq')



class Forwarder
    constructor: (@name, @port, @client_socket) ->
        @socket = zmq.socket('sub')
        @socket.connect('tcp://127.0.0.1:' + @port.toString())
        @socket.subscribe('')
        
    run: ->
        @socket.on('message', (msg) =>
            # message is prefixed by source ID, suffixed by JSON data.
            @data = JSON.parse(msg.toString())
            console.log('Recv msg from ' + @data.name)
            console.log(@data)
            @client_socket.emit(@data.name, @data)
        )
    

### Main ###
console.log 'Qikify: View Server'
io.on('connection', (client_socket) ->
    console.log('Qikify: client has connected')
    client_socket.on('message', (msg) -> console.log('*** Message received from client: ' + msg))
    ateSimForwarder = new Forwarder('atesim', 5001, client_socket)
    ateSimListener.run()
)





