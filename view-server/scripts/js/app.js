var BarChart, Chart, ChartCollection, DOMInteractions, LineChart, init;
var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; }, __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
  for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
  function ctor() { this.constructor = child; }
  ctor.prototype = parent.prototype;
  child.prototype = new ctor;
  child.__super__ = parent.prototype;
  return child;
};
init = function() {
  var d;
  d = new Date();
  window.today = d.toString().split(' GMT')[0];
  console.log(today + " *** Qikify debug");
  window.socket = io.connect('http://localhost:8001');
  window.socket.on('connect', function() {
    window.socket.emit('message', 'Client connected.');
    return console.log('Client requests list of data.');
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
  var barData, barchart, i, lineData, linechart, x, y;
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
  barchart = new BarChart('Histogram', 'Here, we present a histogram of all the data we have acquired thus far.');
  barchart.inject('#data-acquisition');
  barchart.plot(barData);
  linechart = new LineChart('Line Chart', 'Trending upwards.');
  linechart.inject('#data-acquisition');
  return linechart.plot(lineData);
});
DOMInteractions = (function() {
  function DOMInteractions(name) {
    this.name = name;
    this.remove = __bind(this.remove, this);
    this.inject = __bind(this.inject, this);
    this.isRendered = false;
    this.id = null;
  }
  DOMInteractions.prototype.inject = function(parentID, content) {
    if (!this.isRendered) {
      this.isRendered = true;
      this.parentID = parentID;
      return $(parentID).append(content);
    }
  };
  DOMInteractions.prototype.remove = function() {
    if (this.id != null) return $("#" + this.parentID).children(this.id).remove();
  };
  return DOMInteractions;
})();
Chart = (function() {
  __extends(Chart, DOMInteractions);
  function Chart(name, description) {
    this.name = name;
    this.inject = __bind(this.inject, this);
    this.id = Raphael.createUUID();
    this.chart_id = Raphael.createUUID();
    console.log(window.today + (" *** Chart() - " + this.name + " " + this.id));
    this.chartHTML = "<div class=\"row\" id=\"" + this.id + "\">\n  <div class=\"span5\">\n    <h2>" + this.name + "</h2> \n    " + description + "\n  </div>\n  <div class=\"span11\" id=\"" + this.chart_id + "\"></div>\n</div>";
  }
  Chart.prototype.inject = function(parentID) {
    console.log(window.today + " *** Chart.inject");
    Chart.__super__.inject.call(this, parentID, this.chartHTML);
    return this.canvas = Raphael($("#" + this.chart_id)[0], 640, 180);
  };
  return Chart;
})();
BarChart = (function() {
  __extends(BarChart, Chart);
  function BarChart() {
    this.plot = __bind(this.plot, this);
    BarChart.__super__.constructor.apply(this, arguments);
  }
  BarChart.prototype.plot = function(data) {
    return this.canvas.barchart(0, 0, 640, 180, [data.x], 0, {
      type: "square"
    });
  };
  return BarChart;
})();
LineChart = (function() {
  __extends(LineChart, Chart);
  function LineChart() {
    this.plot = __bind(this.plot, this);
    LineChart.__super__.constructor.apply(this, arguments);
  }
  LineChart.prototype.plot = function(data) {
    return this.canvas.linechart(0, 0, 640, 180, data.x, data.y);
  };
  return LineChart;
})();
ChartCollection = (function() {
  function ChartCollection(name) {
    this.name = name;
  }
  ChartCollection.prototype.add = function(name) {
    return console.log('add');
  };
  ChartCollection.prototype.remove = function(name) {
    return console.log('remove');
  };
  return ChartCollection;
})();