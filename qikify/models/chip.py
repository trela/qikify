"""Qikify: Chip model.
"""

class Chip(object):
    """This class encapsulates chip-level data.
    """
    
    def __init__(self, 
                 chip_dict=None, 
                 LCT=None,
                 HCT=None, 
                 gnd=None, 
                 LCT_prefix=''):
        """Expects a dictionary of chip data, chip_dict. A prefix, LCT_prefix,
        is also expected, indicating which parameters are low-cost test data.
        
        Alternatively, the LCT/HCT/gnd values can be provided directly.
        """

        if chip_dict is None:
            self.LCT = LCT
            self.HCT = HCT
            self.gnd = gnd

        else:
            self.LCT = {}
            self.HCT = {}
            self.gnd = 0
            try:
                # create an ID by concatenating wafer ID and XY coordinate.
                self.id = str(chip_dict['WAFER_ID']) + ':' + \
                          str(chip_dict['XY'])
            except:
                self.id = 'unknown_chip_id'
            
            for k in chip_dict:
                if k == "gnd":
                    self.gnd = int(float(chip_dict[k]))
                elif k.startswith(LCT_prefix):
                    self.LCT[k] = chip_dict[k]
                else:
                    self.HCT[k] = chip_dict[k]

