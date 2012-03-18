import os
import zmq
import csv
import pandas
import msgpack
from qikify.models import gz_csv_read

class ATESimulator(object):    
    def __init__(self, data_src='filesystem'):
        """This class is for simulating ATE. It loads data from a data source specified
        by the argument data_src, and emits Chip() model tuples of data.

        """
        self.data_src = data_src
        self.data_dir = None
        self.data     = None

        # ZeroMQ socket stuff
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.PAIR)

    def run(self, port=5570):
        """This function runs the ATE simulator using CSV files in the current directory.

        Currently, we only support loading *.csv or *.csv.gz files.
        """
        print 'Running ATE Simulator on port %d ...' % port

        if self.data_src == 'filesystem':
            import fnmatch
            self.data_dir = os.getcwd()
            file_list    = os.listdir(self.data_dir)
            csv_files    = fnmatch.filter(file_list, '*.csv') 
            csv_gz_files = fnmatch.filter(file_list, '*.csv.gz') 

            if len(csv_files) == 0 and len(csv_gz_files) == 0:
                print 'Error: no data found in current filesystem path'
                return

            elif len(csv_files) > len(csv_gz_files):
                print 'data source: %d csv files...' % len(csv_files)
                self.data  = csv_files
                self.dtype = 'csv'

            else:
                print 'data source: %d csv.gz files...' % len(csv_gz_files)
                self.data  = csv_gz_files
                self.dtype = 'csv.gz'
        else:
            print 'non-filesystem data backends are currently not supported.'

        
        # Run ZeroMQ server
        self.socket.bind('tcp://127.0.0.1:%d' % port)
        try:
            for fname in self.data:
                print fname
                if self.dtype == 'csv':
                    with open(fname, 'r') as f:
                        c = csv.reader(f)
                        header = c.next()
                        self.send_chips(header, c)
                elif self.dtype == 'csv.gz':
                    import gzip, StringIO
                    with gzip.open(fname, 'r') as f:
                        c      = csv.reader(StringIO.StringIO(f.read()))
                        header = c.next()
                        self.send_chips(header, c)
        except KeyboardInterrupt:
            print '\nterminating ATE simulator.'

    def send_chips(self, header, chip_iterable):
        packer = msgpack.Packer()
        for c in chip_iterable:  
            chip = {k : v for k, v in zip(header, c) if v.strip() != ''}
            print '->', chip['WAFER_ID']
            chip_serialized = packer.pack(chip)
            self.socket.send( chip_serialized )












