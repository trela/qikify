import zmq, json, datetime, time
from qikify.controllers.KNN import KNN
from qikify.models.chip import Chip
from qikify.helpers.term_helpers import Colors
from qikify.views.viewserver_mixin import ViewServerMixin


class BasicTesting(ViewServerMixin):
    def __init__(self, port = 5000):
        self.port          = port
        self.chips         = []
        
        self.num_predicted    = 0
        self.num_chips_tested = 0
        self.test_escapes     = 0
        self.yield_loss       = 0
        
        self.is_trained    = False
        
        self.knn           = KNN()
        self.c             = Colors()
        
        # ZeroMQ stuff
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.REQ)
        
        # hand off the ZeroMQ context and port number to the ViewServerMixin
        # superclass, for logging to view server.
        super(BasicTesting, self).__init__('atesim', self.port+2, self.context)
        
        
    def run(self):
        print 'Running Basic Machine learning-based testing,' + \
              'listening on port %d ...' % self.port
        self.socket.connect("tcp://127.0.0.1:%d" % self.port)
        try:
            while True:
                print '[ Train:     %s %7d %s ] ' \
                    % (self.c.GREEN, self.num_train_chips, self.c.ENDC),
                print '[ Predicted: %s %7d %s ]' \
                    % (self.c.GREEN, self.num_predicted, self.c.ENDC)
                    
                self.get_chip()
                self.update_model()
                self.update_view(self.stats)
                
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
        self.num_chips_tested += 1


    def update_model(self):
        """Add the latest chip to the chip buffer. If we've already collected
        1,000 chips, then we go ahead and train the model.
        """
        
        if self.num_chips_tested <= 1000:
            self.chips.append(self.current_chip)
                 
        if self.num_chips_tested == 1000:
            print "Training KNN on 1000 chips"
            self.is_trained = True
            self.knn.fit(self.chips)
            
        if self.num_chips_tested >= 1000:
            time.sleep(0.1)
            self.num_predicted += 1
            chip_gnd_predicted = self.knn.predict(self.current_chip)
            self.log('Actual pf: %d' % self.current_chip.gnd)
            self.log('Pred. pf:  %d' % chip_gnd_predicted)

            # Accounting TE / YL here
            if self.current_chip.gnd == -1 and chip_gnd_predicted == 1:
                self.test_escapes += 1
            if self.current_chip.gnd == 1 and chip_gnd_predicted == -1:
                self.yield_loss += 1
            
    
    def log(self, msg):
        # might expand this later
        print '\t-> %s %s %s' % ( self.c.RED, msg, self.c.ENDC )


    @property
    def num_train_chips(self):
        return len(self.chips)
    
    @property
    def stats(self):
        """The self.update_view() method from the ViewServerMixin class
        expects a Python object that can be JSONified. This function returns 
        such an object.
        """
        return {
                'name' : 'basic',
                'datetime' : datetime.datetime.utcnow().isoformat(),
                'parms' :   
                    {
                        'num_train_chips' : 
                        {
                            'desc' : 'Number of chips in training set',
                            'value': str(self.num_train_chips)
                        },
                        'num_predicted' : 
                        {
                            'desc' : 'Number of chips predicted with k-NN',
                            'value': str(self.num_predicted)
                        },
                        'test_escape' : 
                        {
                            'desc' : 'Test escape rate',
                            #'value': '%1.3f%%' % (self.test_escapes * 100.0 / self.num_chips_tested)
                            'value': (self.test_escapes * 100.0 / self.num_chips_tested)
                        },
                        'yield_loss' : 
                        {
                            'desc' : 'Yield loss rate',
                            #'value': '%1.3f%%' % (self.yield_loss * 100.0 / self.num_chips_tested)
                            'value': (self.yield_loss * 100.0 / self.num_chips_tested)
                        },
                        'is_trained' : 
                        {
                            'desc' : 'Model trained',
                            'value': (lambda (x): 'Yes' if x else 'No')(self.is_trained)
                        }
                    }
                }
                