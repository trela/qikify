"""Qikify ATE Simulator."""

import os, sys, time, zmq, json, fnmatch, fileinput, datetime
from qikify.models.chip import Chip
from qikify.views.viewserver_mixin import ViewServerMixin
from qikify.helpers.term_helpers import Colors

class ChipDataIterator(object):
    """Chip data iterator, abstracts file i/o from csv files of data.
    """
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.header   = None
        self.c        = Colors()
        
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
        line = self.chip_iter.next().strip().split(',')
        if self.chip_iter.filelineno() <= 1:
            # read header line
            self.header = line
            print 'reading from file', self.chip_iter.filename()
            self.n_files_read += 1
            return self.next()
        else:
            # No dict comprehension in python 2.6
            chip_dict = {}
            for k, v in zip(self.header, line):
                if v.strip() != '':
                    chip_dict[k] = v
            # not available in python 2.6
            #chip_dict = {k : v for k, v in zip(self.header, line) if v.strip() != ''}
            
            if 'WAFER_ID' not in chip_dict:
                chip_dict['WAFER_ID'] = self.chip_iter.filename().strip('.csv')
            if 'XY' not in chip_dict:
                chip_dict['XY'] = self.chip_iter.filelineno() - 1

            chip = Chip(chip_dict=chip_dict, LCT_prefix = 'ORB_')
            print '[ %7d ] :%s %s %s' \
                % (self.chip_iter.lineno() - self.n_files_read, 
                   self.c.GREEN, 
                   chip.id,
                   self.c.ENDC)
            return chip
            
                        

class ATESimulator(ViewServerMixin):    
    def __init__(self, port = 5000):
        """This class is for simulating ATE. It loads data from a csv files,
        and emits Chip() model instances of data. 
        """
        self.port = port
        self.c    = Colors()
        
        # ZeroMQ socket stuff
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:%d' % port)
        
        # Internal statistics to track
        self.num_chips_tested = 0
        self.num_lct = 0
        self.num_hct = 0
        self.num_gnd = 0
        
        # hand off the ZeroMQ context and port number to the ViewServerMixin
        # superclass, for logging to view server.
        super(ATESimulator, self).__init__('atesim', self.port+1, self.context)
        
        
    def run(self):
        """This function runs the ATE simulator using CSV files in the current
        directory. Currently, we only support loading .csv or .csv.gz files.
        """
        print 'Running ATE Simulator on port %d ...' % self.port
        try:
            for i, chip in enumerate(ChipDataIterator(os.getcwd())):
                self.num_chips_tested = i + 1
                self.send(chip)
                self.update_view(self.stats)
                
        except KeyboardInterrupt:
            print '\nterminating ATE simulator.'


    def send(self, chip):
        """Send a chip along to the test regime over ZeroMQ socket.
        """
        while True:
            msg  = self.socket.recv()
            print '\t->', self.c.RED, msg, self.c.ENDC
            
            if msg == 'REQ:done':
                self.socket.send('RES:ack')
                break
            
            #time.sleep(0.1)
            
            if msg == 'REQ:LCT':
                data = chip.LCT
                self.num_lct += 1
                
            elif msg == 'REQ:HCT':
                data = chip.HCT
                self.num_hct += 1
                
            elif msg == 'REQ:gnd':
                data = chip.gnd
                self.num_gnd += 1
                
            else:
                break
                                
            self.socket.send( json.dumps(data) )
        sys.stdout.flush()
        return None

    @property
    def stats(self):
        """The self.update_view() method from the ViewServerMixin class
        expects a Python object that can be JSONified. This function returns 
        such an object.
        """
        return {
                'name' : 'atesim',
                'datetime' : datetime.datetime.utcnow().isoformat(),
                'parms' :   
                    {
                        'chips_tested' : {
                                'desc' : 'Number of chips tested',
                                'value': str(self.num_chips_tested)
                        },
                        'perc_lct' : {
                                'desc' : 'Percent of chips tested with LCT',
                                #'value': '%3.1f%%' % (self.num_lct * 100.0 / self.num_chips_tested)
                                'value' : (self.num_lct * 100.0 / self.num_chips_tested)
                        },
                        'perc_gnd' : {
                                'desc' : 'Percent of chips tested completely',
                                #'value': '%3.1f%%' % (self.num_gnd * 100.0 / self.num_chips_tested)
                                'value' : (self.num_gnd * 100.0 / self.num_chips_tested)
                        }
                    }
                }









