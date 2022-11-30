#!/usr/bin/env python3

import argparse
import f90nml

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE1')
    parser.add_argument('FILE2')
    parser.add_argument('-v', '--verbose', action='store_true',
            default=False, help='More Output')
    args = parser.parse_args()
    return args

def compare(nml1, nml2, args, indent=''):
    for key in nml1.keys():
        if args.verbose:
            print(f'{indent} {key}')
        if key not in nml2.keys():
            print(f'{indent}{key} not in nml2')
    for key in nml2.keys():
        if args.verbose:
            print(f'{indent} {key}')
        if key not in nml1.keys():
            print(f'{indent}{key} not in nml1')
        else:
            if type(nml1[key]) != type(nml2[key]):
                print(f'{indent} {key} differ in type: {type(nml1[key])} vs {type(nml2[key])}')
            elif nml1[key] == nml2[key]:
                continue
            elif isinstance(nml1[key], list):
                print(f'{indent}{key}:')
                for val1, val2 in zip(nml1[key], nml2[key]):
                    print(f'{indent}  {val1} vs {val2}')
            elif isinstance(nml1[key], f90nml.Namelist):
                print(f'{indent}{key}:')
                compare(nml1[key], nml2[key], args, indent+'  ')
            elif nml1[key] != nml2[key]:
                print(f'{indent}{key} differ: {nml1[key]} vs {nml2[key]}')
                print(f'{indent} (types: {type(nml1[key])})')


def main():
    args = parseargs()
    if args.verbose:
        print(args)

    nml1 = f90nml.read(args.FILE1)
    nml2 = f90nml.read(args.FILE2)

    compare(nml1, nml2, args)


if __name__ == '__main__':
    main()
