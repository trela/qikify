import zmq, json, time
from qikify.controllers.KNN import KNN
from qikify.models.chip import Chip

class BasicTesting(object):
    def __init__(self, port = 5000):
        self.port = port
        self.knn = KNN()
        self.chips = []
        
        # ZeroMQ stuff
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.REQ)
        
    def run(self):
        print 'Running Basic Machine learning-based testing,' + \
              'listening on port %d ...' % self.port
        self.socket.connect("tcp://127.0.0.1:%d" % self.port)
        try:
            while True:
                print '[ %7d ]' % (self.recv_count + 1)
                self.get_chip()
                self.update_model()
        except KeyboardInterrupt:
            print '\nterminating basic ML testing.'


    def get_chip(self):
        """Request and retrieve a chip from the ATE simulator.
        """
        
        self.socket.send('REQ:LCT')
        chip_lct = json.loads(self.socket.recv())
        self.log('REQ:LCT')
        
        self.socket.send('REQ:gnd')
        chip_gnd = json.loads(self.socket.recv())
        self.log('REQ:gnd')

        self.socket.send('REQ:done')
        assert self.socket.recv() == 'RES:ack', \
            'Error: invalid ack from ATE simulator'
        self.log('REQ:done')
        self.current_chip = Chip(LCT=chip_lct, gnd=chip_gnd)


    def update_model(self):
        """Add the latest chip to the chip buffer. If we've already collected
        1,000 chips, then we go ahead and train the model.
        """
        
        if self.recv_count <= 1000:
            self.chips.append(self.current_chip)
                 
        if self.recv_count == 1000:
            print "Training KNN on 1000 chips"
            self.knn.fit(self.chips)
            
        if self.recv_count > 1000:
            self.knn.predict(chip)

    
    def log(self, msg):
        # might expand this later
        print '\t->', msg


    @property
    def recv_count(self):
        return len(self.chips)
        
