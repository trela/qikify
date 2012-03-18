#from qikify.models.dataset import Dataset
#from qikify.models.specs import Specs
#from qikify.models.dotdict import dotdict

from chip import Chip

def gz_csv_read(file_path, pandasDF=False):
    import csv
    import gzip
    from StringIO import StringIO
    with gzip.open(file_path, 'r') as f:
        if pandasDF:
            import pandas
            data = pandas.read_csv(StringIO(f.read()))
        else:
            reader = csv.reader(StringIO(f.read()))
            data   = [row for row in reader]
    return data

def gz_csv_write(file_path, data):
    import csv
    import gzip
    from StringIO import StringIO
    import pandas
    with gzip.open(file_path, 'w') as f:
        if isinstance(data, pandas.DataFrame):
            data.to_csv(file_path, index=False)
        else:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

