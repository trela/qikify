"""Qikify: Chip model.
"""

class Chip(object):
    """This class encapsulates chip-level data.
    """
    def __init__(self, chip_dict, LCT_prefix = ''):
        """Expects a dictionary of chip data. A prefix indicating which
        parameters are low-cost test data is also expected."""

        self.LCT = {}
        self.HCT = {}
        try:
            self.id = chip_dict['WAFER_ID'] + ':' + chip_dict['XY']
        except:
            self.id = 'unknown_chip_id'

        for k in chip_dict:
            if k.startswith(LCT_prefix):
                self.LCT[k] = chip_dict[k]
            else:
                self.HCT[k] = chip_dict[k]

