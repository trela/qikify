class DOMInteractions
    constructor: (@name) ->
        @isRendered = false
        @id = Raphael.createUUID()
    inject: (@parentID, content) =>
        if not @isRendered
            @isRendered = true
            $(parentID).append(content)
    remove: =>
        if @id?
            $("#" + @parentID).children(@id).remove()


class Section extends DOMInteractions
    constructor: (@name, @header, @subheader, @hasStatSection) ->
        super
        console.log window.today + " *** Section() - #{@name} #{@id}"
        @sectionHTML = """
            <section id="#{ @id }">
                <div class="page-header">
                    <h1>#{ @header } <small>#{ @subheader }</small></h1>
                </div>
            </section>"""
        @inject '#main'
        
        if @hasStatSection
            @statSection = new StatCollection(@name, @id) 
            
    inject: (parentID) =>
        console.log window.today + " *** Section.inject"
        super parentID, @sectionHTML