"""Qikify: model helper functions.
"""

def gz_csv_read(file_path, use_pandas=False):
    """Read a gzipped csv file.
    """
    import csv
    import gzip
    from StringIO import StringIO
    with gzip.open(file_path, 'r') as infile:
        if use_pandas:
            import pandas
            data = pandas.read_csv(StringIO(infile.read()))
        else:
            reader = csv.reader(StringIO(infile.read()))
            data   = [row for row in reader]
    return data

def gz_csv_write(file_path, data):
    """Write a gzipped csv file.
    """
    import csv, gzip, pandas
    with gzip.open(file_path, 'w') as outfile:
        if isinstance(data, pandas.DataFrame):
            data.to_csv(file_path, index=False)
        else:
            writer = csv.writer(outfile)
            for row in data:
                writer.writerow(row)

