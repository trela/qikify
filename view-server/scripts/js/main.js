var Statistic, init;
var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
Statistic = (function() {
  function Statistic(name) {
    this.name = name;
    this.update = __bind(this.update, this);
    this.inject = __bind(this.inject, this);
    this.isRendered = false;
    this.id = Raphael.createUUID();
    console.log(window.today + (" *** Statistic() - " + this.name + " " + this.id));
  }
  Statistic.prototype.inject = function(parentID, selfID) {
    var statHTML;
    console.log(window.today + " *** Statistic.inject");
    statHTML = "<p class=\"statistic\">\n    " + this.name + ": \n    <span class=\"statistic-value\" id=" + this.id + ">\n    </span>\n</p>";
    if (!this.isRendered) {
      this.isRendered = true;
      this.parentID = parentID;
      this.selfID = selfID;
      return $(parentID).append(statHTML);
    }
  };
  Statistic.prototype.update = function(statistic) {
    return $('#' + this.id).text(statistic);
  };
  return Statistic;
})();
init = function() {
  var d;
  d = new Date();
  window.today = d.toString().split(' GMT')[0];
  console.log(today + " *** Qikify debug");
  window.socket = io.connect('http://localhost:8001');
  window.socket.on('connect', function() {
    return window.socket.emit('message', 'Client connected.');
  });
  $("#data-getter-modal").modal({
    keyboard: true,
    backdrop: true
  });
  return $('#data-getter-modal').bind('show', function() {
    console.log('Requesting data');
    window.socket.emit('message', 'Client requests list of data.');
    return socket.emit('list', function(data) {
      var d, datasets, _i, _len;
      if (data != null) {
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          d = data[_i];
          datasets = " " + d + " ";
        }
        console.log(data);
        return $('p#lists').text(datasets);
      } else {
        return console.log('No datasets found.');
      }
    });
  });
};
$(function() {
  var atestat, barData, i, lineData, linechart, x, y;
  init();
  barData = {
    "x": [55, 20, 13, 32, 5, 1, 2, 10, 55, 20, 13, 32, 5, 1, 2, 10, 55, 20, 13, 32, 5, 1, 2, 10]
  };
  x = [];
  y = [];
  i = 0;
  while (i !== 1e3) {
    x[i] = i * 10;
    y[i] = (y[i - 1] || 0) + (Math.random() * 7) - 3;
    i += 1;
  }
  lineData = {
    x: x,
    y: y
  };
  linechart = new LineChart('Line Chart', 'Trending upwards.');
  linechart.inject('#ate-sim');
  linechart.plot(lineData);
  atestat = new Statistic('Number of chips tested');
  atestat.inject('#statistics > div');
  window.socket.on('atesim', __bind(function(v) {
    return atestat.update(v.statistic);
  }, this));
  return window.atestat = atestat;
});