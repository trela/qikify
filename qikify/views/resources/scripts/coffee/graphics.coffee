   
class Chart extends DOMInteractions
    # This creates the HTML for a chart in the page.
    constructor: (@name, @description, @chart_id) ->
        super
        console.log window.today + " *** Chart() - #{@name} #{@id}"
        @canvas = Raphael($("#" + @chart_id)[0], 600, 80)
        
class BarChart extends Chart
    plot: (data) =>
        @canvas.barchart(0, 0, 640, 180, [data.x], 0, {type: "square"});

class LineChart extends Chart
    constructor: (@name, @description, @parentID) ->
        super @name, @description, @parentID
        @data = {"x": [], "y": []}
        @recv_msg_count = 0
        
    plot: () =>
        @canvas.clear()
        @chart = @canvas.linechart(0, 0, 600, 80, @data.x, @data.y)
    
    update: (yval) =>
        @data.x = [0..@recv_msg_count]
        @data.y.push yval
        @recv_msg_count += 1
        
        # We only plot if we've gotten at least two messages
        if @recv_msg_count > 1
            @plot()
        
            


class HLineChart
    constructor: (@parentID) ->
        console.log window.today + " *** HLineChart()"
        @data = [{
            name: '',
            data: (() =>
                # generate an array of random data
                data = []
                for i in [-19..0]
                    data.push {
                        x: (new Date()).getTime() + i * 1000,
                        y: 0
                    }
                return data
            )()
        }]

        @chart = new Highcharts.Chart({
            chart: {
                renderTo: @parentID,
                type: 'line',
            },
            legend: { enabled: false },
            exporting: { enabled: false },
            credits : { enabled : false },
            title: { text: '' },
            xAxis: { type: 'datetime', tickPixelInterval: 150 },
            yAxis: {
                title: { text: '' },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            series: @data
        })

    update: (y) ->
        console.log window.today + " *** HLineChart().update()"
        x = (new Date()).getTime()
        console.log x, Number(y)
        @chart.series[0].addPoint([x, Number(y)], true, true)


