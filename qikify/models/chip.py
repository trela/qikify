
class Chip(object):
    import pandas
    def __init__(self, chip_dict=None, LCT=None, HCT=None, gnd=None, LCT_prefix=''):
        """Expects a dictionary of chip data. A prefix indicating which 
        parameters are low-cost test data is also expected."""

        if chip_dict is None:
            self.LCT = LCT
            self.HCT = HCT
            self.gnd = gnd

        else:
            
            self.LCT = {}
            self.HCT = {}
            self.gnd=0
            try:
                self.id = chip_dict['WAFER_ID'] + ':' + chip_dict['XY']
            except:
                self.id = 'unknown_chip_id'


            for k in chip_dict:
                if k=="gnd":
                    self.gnd=chip_dict[k]
                elif k.startswith(LCT_prefix):
                    self.LCT[k] = chip_dict[k]
                else:
                    self.HCT[k] = chip_dict[k]

