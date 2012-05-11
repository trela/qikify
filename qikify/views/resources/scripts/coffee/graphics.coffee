
            


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


