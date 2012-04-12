
import zmq
import msgpack
import time
from qikify.controllers.KNN import KNN
from qikify.models import Chip

class BasicMLTesting(object):
    def __init__(self):
        self.chip_buffer = []
        self.recv_count = 0
        self.knn = KNN()

    def run(self, port = 5570):
        self.port = port

        print 'Running Basic Machine learning-based testing, listening on port %d ...' % port
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:5570")

        unpacker = msgpack.Unpacker()
        try:
            while True:
                print 'Requesting chip instance ...',

                self.socket.send('REQ:send_LCT')
                unpacker.feed(self.socket.recv())
                chip_lct = unpacker.unpack()
                
                # assert self.socket.recv() == 'RES:ack', \
                #         'Error: invalid ack from ATE simulator'
                # print chip_lct
                # time.sleep(10)
                self.socket.send('REQ:send_gnd')
                unpacker.feed(self.socket.recv())
                chip_gnd =unpacker.unpack()

                chip = Chip(LCT=chip_lct, gnd=chip_gnd)

                if self.recv_count<=1000 and chip is not None:
                    self.recv_count += 1
                    self.chip_buffer.append(chip)
                    print 'received chip #', self.recv_count

                    print 'sending done to ATE simulator ...\n'
                    self.socket.send('REQ:done')
                    assert self.socket.recv() == 'RES:ack', \
                        'Error: invalid ack from ATE simulator'
                if self.recv_count==1000:
                    #recv_count=0
                    print "Training Algorithm will run on these 1000 chips"
                    self.knn.trainmodel(self.chip_buffer)
                if self.recv_count > 1000:
                    self.knn.predict(chip)

        except KeyboardInterrupt:
            print '\nterminating basic ML testing.'
