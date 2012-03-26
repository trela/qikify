
class Chip(object):
    import pandas
    def __init__(self, chip_dict, LCT_prefix = ''):
        """Expects a dictionary of chip data. A prefix indicating which 
        parameters are low-cost test data is also expected."""

        self.LCT = {}
        self.HCT = {}
        self.gnd=0
        try:
            self.id = chip_dict['WAFER_ID'] + ':' + chip_dict['XY']
        except:
            self.id = 'unknown_chip_id'

        import pdb; pdb.set_trace()
        
        for k in chip_dict:
            if k=="gnd":
                self.gnd=chip_dict[k]
            if k.startswith(LCT_prefix):
                self.LCT[k] = chip_dict[k]
            else:
                self.HCT[k] = chip_dict[k]

