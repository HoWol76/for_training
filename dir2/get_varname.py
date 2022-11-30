#!/usr/bin/env python3

import argparse
import xarray as xr

class Stashcode:
    def __init__(self, model, section, item):
        self.model = model
        self.section = section
        self.item = item
    def __str__(self):
        return f'm{self.model:02}s{self.section:02}i{self.item:03}'

def find_stashcode(var, sc):
    if 'um_stash_source' in var.attrs:
        if f'm{sc.model:02}s{sc.section:02}i{sc.item:03}' == var.attrs['um_stash_source']:
            return True
    if 'stash_model' in var.attrs and 'stash_section' in var.attrs and 'stash_item' in var.attrs:
        return (var.attrs['stash_model'] == sc.model and
                var.attrs['stash_section'] == sc.section and
                var.attrs['stash_item'] == sc.item)
    pass


def find_stashcode_list(var, scs):
    for sc in scs:
        if find_stashcode(var, sc):
            return True
    return False


def convert_stashcode(raw_stashcode):
    if len(raw_stashcode) == 5:
        model = 1
        section = int(raw_stashcode[:2])
        item = int(raw_stashcode[2:])
    elif len(raw_stashcode) == 6:
        model = int(raw_stashcode[0])
        section = int(raw_stashcode[1:3])
        item = int(raw_stashcode[3:])
    return Stashcode(model, section, item)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-s', '--stashcode', type=str, nargs='*')
    args = parser.parse_args()
    sc = [convert_stashcode(code) for code in args.stashcode]
    ds = xr.open_dataset(args.file)
    varlist = []
    for var in ds:
        if find_stashcode_list(ds[var], sc):
            varlist.append(var)
    print(",".join(varlist))

if __name__ == '__main__':
    main()
