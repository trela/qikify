init = () ->
    # Set up date
    d = new Date()
    window.today = d.toString().split(' GMT')[0]
    console.log today + " *** Qikify debug"
    
    # socket.io stuff here
    window.socket = io.connect('http://localhost:8001')
    window.socket.on('connect', () ->
        window.socket.emit('message', 'Client connected.')
        console.log 'Client requests list of data.'
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
    
    
    barchart = new BarChart('Histogram', 'Here, we present a histogram of all the data we have acquired thus far.')
    barchart.inject('#data-acquisition')
    barchart.plot(barData)
    
    linechart = new LineChart('Line Chart', 'Trending upwards.')
    linechart.inject('#data-acquisition')
    linechart.plot(lineData)
    
    