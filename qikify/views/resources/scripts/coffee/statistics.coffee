
class Statistic extends DOMInteractions
    # This class creates the HTML for a statistic in the page.
    constructor: (@name) ->
        super
        console.log window.today + " *** Statistic() - #{@name} #{@id}"
        @statHTML = """
        <p class="stat" id=#{ @id }>
            <span class="stat-label"></span>
            <span class="stat-value"></span>
        </p>
        """
        
    inject: (parentID) =>
        console.log window.today + " *** Statistic.inject"
        super parentID, @statHTML
            
    update: (msg) =>
        console.log window.today + " *** Statistic.update #{ msg.desc } - #{ msg.value }"
        $('#' + @id + ' > span.stat-label').text(msg.desc + ':')
        $('#' + @id + ' > span.stat-value').text(msg.value)
        


class StatCollection
    constructor: (@name, @parentID) ->
        @id = Raphael.createUUID()
        console.log window.today + " *** StatCollection() - #{@name} #{@id}"
        @isRendered = false
        @stats = {}
        @statHTML = """
        <div class="row statistics" id = "#{ @id }">
          <div class="span16">
            <h2>Statistics</h2>
          </div>
        </div>"""
        
        window.socket.on('message', (v) =>
            if v.name == @name
                if not @isRendered
                    $('#' + @parentID).append(@statHTML)
                    @isRendered = true
                    @inject('#' + @parentID + ' > .statistics > div', p for p of v.parms)
                    
                for k, par of v.parms
                    @stats[k].update(par)
        )
    
    inject: (parentID, parms) =>
        for k in parms
            s = new Statistic("#{ @name }:#{ k }")
            s.inject(parentID)    
            @stats[k] = s
        





