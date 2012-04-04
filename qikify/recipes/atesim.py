import os
import time
import zmq
import csv
import pandas
import msgpack
import fnmatch
import fileinput
from qikify.models import Chip, gz_csv_read


class ChipDataIterator(object):
    def __init__(self, data_dir):
        self.data_dir = data_dir
        file_list    = os.listdir(self.data_dir)
        csv_files    = fnmatch.filter(file_list, '*.csv') 
        csv_gz_files = fnmatch.filter(file_list, '*.csv.gz') 

        assert len(csv_files) > 0 or len(csv_gz_files) > 0, \
               'Error: no data found in filesystem path'

        if len(csv_files) > len(csv_gz_files):
            print 'data source: reading %d csv files...' % len(csv_files)
            self.data  = csv_files
        else:
            print 'data source: reading %d csv.gz files...' % len(csv_gz_files)
            self.data  = csv_gz_files

        # this iterator points to the latest chip from the latest wafer file.
        self.chip_iter = fileinput.input(self.data) 

        self.n_files_read = 0


    def __iter__(self):
        return self


    def next(self):
        """The call to self.chip_iter.next() will raise StopIteration when done, 
        propagating through to the caller of ChipDataIterator().next().
        """
        line = self.chip_iter.next().split(',')
        if self.chip_iter.filelineno() <= 1:
            # read header line
            self.header = line
            print 'reading from file', self.chip_iter.filename()
            self.n_files_read += 1
            return self.next()
        else:
            print '[ %7d ]' % (self.chip_iter.lineno() - self.n_files_read),
            chip_dict = {k : v for k, v in zip(self.header, line) if v.strip() != ''}
            return Chip(chip_dict=chip_dict, LCT_prefix = 'ORB_')

                        

class ATESimulator(object):    
    def __init__(self, data_src='filesystem'):
        """This class is for simulating ATE. It loads data from a data source specified
        by the argument data_src, and emits Chip() model tuples of data.

        """
        self.data_src = data_src

        # ZeroMQ socket stuff
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.REP)

    def run(self, port=5570):
        """This function runs the ATE simulator using CSV files in the current directory.
        Currently, we only support loading *.csv or *.csv.gz files.
        """

        print 'Running ATE Simulator on port %d ...' % port

        if self.data_src != 'filesystem':
            print 'non-filesystem data backends are currently not supported.'
            return
        
        # Run ZeroMQ server
        self.socket.bind('tcp://127.0.0.1:%d' % port)
        packer = msgpack.Packer()
        try:
            for chip in ChipDataIterator(os.getcwd()):
                while True:
                    msg  = self.socket.recv()
                    print '->', chip.id, msg, 
                    if msg == 'REQ:send_LCT':
                        # send chip low-cost test data
                        print 'lct', 
                        #time.sleep(1)
                        chip_serialized = packer.pack(chip.LCT)
                        self.socket.send( chip_serialized )
                    elif msg == 'REQ:send_HCT':
                        # send chip high-cost test data
                        print 'LCT', 
                        #time.sleep(1)
                        chip_serialized = packer.pack(chip.HCT)
                        self.socket.send( chip_serialized )
                    elif msg == 'REQ:send_gnd':
                        #send chip gnd test values
                        print 'gnd'
                        #time.sleep(1)
                        chip_serialized=packer.pack(chip.gnd)
                        self.socket.send( chip_serialized )
                    elif msg == 'REQ:done':
                        print 'done.'
                        self.socket.send('RES:ack')
                        break
                    else:
                        print 'invalid message---continuing to next chip.'
                        break
                    print '\n           ',

        except KeyboardInterrupt:
            print '\nterminating ATE simulator.'









