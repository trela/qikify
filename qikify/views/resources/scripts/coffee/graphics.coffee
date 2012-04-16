   
class Chart extends DOMInteractions
    # This creates the HTML for a chart in the page.
    constructor: (@name, description) ->
        super
        @chart_id = Raphael.createUUID()
        console.log window.today + " *** Chart() - #{@name} #{@id}"
        @chartHTML = """
                     <div class="row" id="#{@id}">
                       <div class="span5">
                         <h2>#{@name}</h2> 
                         #{description}
                       </div>
                       <div class="span11" id="#{@chart_id}"></div>
                     </div>
                     """
        
    inject: (parentID) =>
        console.log window.today + " *** Chart.inject"
        super parentID, @chartHTML
        @canvas = Raphael($("#" + @chart_id)[0], 640, 180)

        
class BarChart extends Chart
    plot: (data) =>
        @canvas.barchart(0, 0, 640, 180, [data.x], 0, {type: "square"});

class LineChart extends Chart
    plot: (data) =>
        @canvas.linechart(0, 0, 640, 180, data.x, data.y)
        

class ChartCollection
    constructor: (@name) ->
        # something like "chart_array.push_back(new_chart) for i in range(10)" here
        # Will create a <section> with charts in page.
        
        # Bar chart
        barData = {"x": [55, 20, 13, 32, 5, 1, 2, 10, 55, 20, 13, 32, 5, 1, 2, 10, 55, 20, 13, 32, 5, 1, 2, 10]};

        # Line chart
        x = []
        y = []
        i = 0
        until i == 1e3
            x[i] = i * 10;
            y[i] = (y[i - 1] || 0) + (Math.random() * 7) - 3;
            i += 1
        lineData = {x: x, y: y}

        #barchart = new BarChart('Histogram', 'Here, we present a histogram of all the data we have acquired thus far.')
        #barchart.inject('#data-acquisition')
        #barchart.plot(barData)

        # linechart = new LineChart('Line Chart', 'Trending upwards.')
        # linechart.inject('#ate-sim')
        # linechart.plot(lineData)

    add: (name) ->
        console.log 'add' #add a chart here
        
    remove: (name) ->
        console.log 'remove' # remove a chart here
        
        
