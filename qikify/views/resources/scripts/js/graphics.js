var BarChart, Chart, ChartCollection, DOMInteractions, LineChart;
var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; }, __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
  for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
  function ctor() { this.constructor = child; }
  ctor.prototype = parent.prototype;
  child.prototype = new ctor;
  child.__super__ = parent.prototype;
  return child;
};
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