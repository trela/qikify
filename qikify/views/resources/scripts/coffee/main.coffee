init = () ->
    # Set up date
    d = new Date()
    window.today = d.toString().split(' GMT')[0]
    console.log today + " *** Qikify debug"
    
    # socket.io stuff here
    window.socket = io.connect('http://localhost:8001')
    window.socket.on('connect', () ->
        window.socket.emit('message', 'Client connected.')
    )
    
    # Set up modal dialog
    $("#data-getter-modal").modal({
        keyboard: true, 
        backdrop: true
    })
    
    # When the "Get data" dialog is clicked, we query the server async for
    # a list of datasets.
    $('#data-getter-modal').bind('show', () ->
        console.log('Requesting data')
        window.socket.emit('message', 'Client requests list of data.')
        socket.emit('list', (data) ->
            if data?
                datasets = " "+d+" " for d in data
                console.log data
                $('p#lists').text(datasets) #[" " + data for data in datasets])
            else
                console.log 'No datasets found.'
        )
    )

$ ->
    init()
    ateSection = new Section('atesim', 
                             'ATE Simulator', 
                             'updates from the ATE simulator',
                             true)
    testSection = new Section('basic', 
                              'Basic Tester', 
                              'updates from the test plan',
                              false)
