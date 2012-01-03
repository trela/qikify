var io = require('socket.io').listen(8001);


// Generate datasets
var x = []
  , y = []
  , i = 0;
for (var i = 0; i < 1e3; i++) {
    x[i] = i * 10;
    y[i] = (y[i - 1] || 0) + (Math.random() * 7) - 3;    
}
datasets = ["raw tester data", "another tester dataset"];

data = {"barData" : {"x": [55, 20, 13, 32, 5, 1, 2, 10, 55, 20, 13, 32, 5, 1, 2, 10, 55, 20, 13, 32, 5, 1, 2, 10]},                                                                                     // y
            "lineData": {"x": x,
                         "y": y}};

io.sockets.on('connection', function (socket) {
    socket.emit('message', 'Connected to web socket server.');
    
    // Log other messages
    socket.on('message', function(msg) {
        console.log('*** Message received from client: ' + msg);
        //if (msg == 'list') {
        //    socket.emit('message', JSON.stringify(datasets));
        //}
    });
    socket.on('list', function(fn) {
        console.log(fn);
        fn(datasets);
    });
});

