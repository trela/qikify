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
    Highcharts.setOptions({
            global: { useUTC: false }
    })
        
$ ->
    init()
    window.ateSection = new Section('atesim', 
                             'ATE Simulator', 
                             'updates from the ATE simulator')
    testSection = new Section('basic', 
                              'Basic Tester', 
                              'updates from the test plan')
