class DOMInteractions
    constructor: (@name) ->
        @isRendered = false
        @id         = null
    inject: (parentID, content) =>
        if not @isRendered
            @isRendered = true
            @parentID   = parentID
            $(parentID).append(content)
    remove: =>
        if @id?
            $("#" + @parentID).children(@id).remove()
            
    
class Chart extends DOMInteractions
    # This creates the HTML for a chart in the page.
    constructor: (@name, description) ->
        @id       = Raphael.createUUID()
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
        
    add: (name) ->
        console.log 'add' #add a chart here
        
    remove: (name) ->
        console.log 'remove' # remove a chart here
        
        
