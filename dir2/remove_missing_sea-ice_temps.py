#!python

import sys
import mule
import numpy.ma as ma


class RemoveMissing(mule.DataOperator):
    """
    Remove missing data from a field, setting to average value
    """
    def __init__(self):
        pass

    def new_field(self, source_field):
        return source_field.copy()

    def transform(self, source_field, result_field):
        data = source_field.get_data()
        masked = ma.masked_values(data, source_field.bmdi)
        return masked.filled(masked.mean())

def validate(filename=None, warn=False):
    pass

rem_missing = RemoveMissing()

data = mule.load_umfile(sys.argv[1])

for i,f in enumerate(data.fields):
    if f.lbuser4 == 49:
        data.fields[i] = rem_missing(f)

data.validate = validate
data.to_file(sys.argv[2])
