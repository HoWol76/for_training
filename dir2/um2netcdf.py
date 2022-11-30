#!/usr/bin/env python3

import argparse
import numpy as np
import iris


def args_parse():
    parser = argparse.ArgumentParser('Converts UM files to NetCDF')
    parser.add_argument('-i', '--input', type=str, help='input file',
            required=True)
    parser.add_argument('-o', '--output', type=str, help='output file',
            required=True)
    parser.add_argument('-f', '--float', 
            help='save as 32bit values', action='store_true', 
            default=False)
    parser.add_argument('-z', '--compress', type=int, help='compression level', 
            default=4)
    return parser.parse_args()


def main():
    args = args_parse()
    cubes = iris.load(args.input)
    if args.float:
        for cube in cubes:
            cube.data = cube.data.astype(np.float32)
    iris.fileformats.netcdf.save(cubes, 
            filename=args.output,
            zlib=(args.compress>0),
            complevel=args.compress,
            shuffle=True
            )


if __name__ == '__main__':
    main()
