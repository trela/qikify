(function() {
  var datasets, fs, http, i, io, x, y;
  console.log('Qikify View Server');
  io = require('socket.io').listen(8001);
  fs = require('fs');
  http = require('http');
  x = [];
  y = [];
  i = 0;
  while (i < 1e3) {
    x[i] = i * 10;
    y[i] = (y[i - 1] || 0) + (Math.random() * 7) - 3;
    i++;
  }
  datasets = ["raw tester data", "another tester dataset"];
  io.sockets.on('connection', function(socket) {
    var logFile;
    socket.emit('message', 'Connected to web socket server.');
    socket.on('message', function(msg) {
      return console.log('*** Message received from client: ' + msg);
    });
    socket.on('list', function(fn) {
      console.log(fn);
      return fn(datasets);
    });
    console.log("Watching qikify logs");
    logFile = '/tmp/qikify/qikify.recipes.ATESimulator.log';
    return fs.watch(logFile, function(event, filename) {
      return fs.readFile(logFile, function(err, data) {
        var lines;
        if (err) console.log(err);
        lines = data.toString().split("\n");
        console.log("Found %d lines", lines.length);
        return socket.emit('atesim', {
          statistic: lines.length
        });
      });
    });
  });
}).call(this);
