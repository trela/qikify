class DOMInteractions
    constructor: (@name) ->
        @isRendered = false
        @id = Raphael.createUUID()
        
    inject: (@parentID, content) =>
        if not @isRendered
            @isRendered = true
            $('#' + @parentID).append(content)
            
    remove: =>
        if @id?
            $("#" + @parentID).children(@id).remove()


class Statistic extends DOMInteractions
    # This class creates the HTML for a statistic in the page.
    constructor: (@name, @parentID) ->
        super
        console.log window.today + " *** Statistic() - #{@name} #{@id}"
        @statHTML = """
        <p class="stat" id=#{ @id }>
            <span class="stat-label"></span>
            <span class="stat-value"></span>
        </p>
        """
        @inject(@parentID, @statHTML)

    update: (msg) =>
        console.log window.today + " *** Statistic.update #{ msg.desc } - #{ msg.value }"
        $('#' + @id + ' > span.stat-label').text(msg.desc + ':')
        $('#' + @id + ' > span.stat-value').text(msg.value)



class Parameter extends DOMInteractions
    constructor: (@name, @desc, @parentID) ->
        super
        console.log window.today + " *** Parameter()"
        @stats_id = Raphael.createUUID()
        @chart_id = Raphael.createUUID()
        @parmHTML = """<div class="row">
          <div class="span16"><h2>#{@desc}</h2></div>
          <div class="span5"  id="#{@stats_id}"></div>
          <div class="span11" id="#{@chart_id}" style="min-width: 400px; height: 150px; margin: -5px auto"></div></div>"""
        @inject @parentID, @parmHTML
        
        # maintain statistics
        @stat  = new Statistic(@name, @stats_id)
        @chart = new HLineChart(@chart_id)

    update: (par) =>
        console.log window.today + " *** Parameter().update()"
        @stat.update({'desc': 'Current Value', 'value': par.value})
        @chart.update(par.value)

        
        
class Section extends DOMInteractions
    constructor: (@name, @header, @subheader) ->
        super
        console.log window.today + " *** Section() - #{@name} #{@id}"
        
        # Assemble HTML template for section
        @sectionHTML = """
            <section id="#{ @id }">
                <div class="page-header">
                    <h1>#{ @header } <small>#{ @subheader }</small></h1>
                </div>
                
            </section>"""
        @inject 'main', @sectionHTML

        @parms = {}
        
        # @test_stat = {'desc' : 'Number of chips tested', 'value': '910'}
        # @parm = new Parameter('atesim:chips_tested', @test_stat.desc, @id)
        # @test_stat2 = {'desc' : 'Number of chips tested', 'value': '1023'}
        # @test_stat3 = {'desc' : 'Number of chips tested', 'value': '996'}
        # @parm.update(@test_stat)
        # @parm.update(@test_stat2)
        # @parm.update(@test_stat3)
        # @parm.update(@test_stat)
        # @parm.update(@test_stat3)
        
        # Listen for JSON with name property set to same as class @name property
        window.socket.on('message', (v) =>
            if v.name == @name
                # iterate over parms
                for k, par of v.parms
                    if not @parms.hasOwnProperty(k)
                        @parms[k] = new Parameter("#{ @name }:#{ k }", par.desc, @id)
                    @parms[k].update(par)
        )






