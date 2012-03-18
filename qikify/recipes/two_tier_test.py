import zmq
import msgpack
import time

class TwoTierTest(object):
    def __init__(self):
        self.chip_buffer = []
        self.recv_count = 0

    def run(self, port = 5570):
        self.port = port

        print 'Running 2 Tier Test, listening on port %d ...' % port
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://127.0.0.1:5570")
        try:
            while True:
                unpacker = msgpack.Unpacker()
                unpacker.feed(self.socket.recv())
                chip = unpacker.unpack()
                if chip is not None:
                    self.recv_count += 1
                self.chip_buffer.append(chip)   
                print 'Received chip #', self.recv_count
        except KeyboardInterrupt:
            print '\nterminating 2 Tier Test.'