console.log 'Qikify View Server'

io = require('socket.io').listen(8001)
fs = require('fs')                                                                     
http = require('http')


# Generate datasets
x = []
y = []
i = 0
while i < 1e3
    x[i] = i * 10
    y[i] = (y[i - 1] or 0) + (Math.random() * 7) - 3
    i++  
datasets = ["raw tester data", "another tester dataset"]
io.sockets.on('connection', (socket) ->
    socket.emit('message', 'Connected to web socket server.')    
    socket.on('message', (msg) -> console.log('*** Message received from client: ' + msg))
    socket.on('list', (fn) ->
        console.log(fn)
        fn(datasets)
    )
    
    ## Watch log files
    console.log("Watching qikify logs");
    logFile = '/tmp/qikify/qikify.recipes.ATESimulator.log'
    fs.watch(logFile, (event, filename) ->
        fs.readFile(logFile, (err, data) ->
            if (err) 
                console.log err
            lines = data.toString().split("\n")
            console.log("Found %d lines", lines.length)
            socket.emit('atesim', { statistic: lines.length })
        )
    )
)





