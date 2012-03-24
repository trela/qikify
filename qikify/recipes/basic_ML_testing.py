import zmq
import msgpack
import time

class BasicMLTesting(object):
    def __init__(self):
        self.chip_buffer = []
        self.recv_count = 0

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
                chip = unpacker.unpack()
                if chip is not None:
                    self.recv_count += 1
                    self.chip_buffer.append(chip)
                    print 'received chip #', self.recv_count

                    print 'sending done to ATE simulator ...\n'
                    self.socket.send('REQ:done')
                    assert self.socket.recv() == 'RES:ack', \
                        'Error: invalid ack from ATE simulator'
                if self.recv_count==1000:
                    print "Training Algorithm will run on these 1000 chips"

        except KeyboardInterrupt:
            print '\nterminating basic ML testing.'
