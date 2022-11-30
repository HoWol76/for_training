#!/usr/bin/env python3

import argparse
import deepdiff
import f90nml

def my_parse():
    parser = argparse.ArgumentParser('Compare two Namelists')
    parser.add_argument('file1')
    parser.add_argument('file2')
    parser.add_argument('-v', '--verbose', action='store_true',
            default=False, help="print additional output")
    return parser.parse_args()

def parse_item(item):
    namelist = item.split("'")[1]
    variable = item.split("'")[3]
    return namelist, variable

def main():
    args = my_parse()

    if args.verbose:
        print(args)

    nml1 = f90nml.read(args.file1)
    nml2 = f90nml.read(args.file2)

    diff = deepdiff.DeepDiff(nml1, nml2)
    for category in diff.keys():
        if (category == 'dictionary_item_added'):
            print("Values Added:")
            for item in diff[category]:
                namelist, variable = parse_item(item)
                print(f'  (N)  {namelist} > {variable}    ({nml2[namelist][variable]})')
        elif (category == 'dictionary_item_removed'):
            print("Values Removed:")
            for item in diff[category]:
                namelist, variable = parse_item(item)
                print(f'  (D)  {namelist} > {variable}    ({nml1[namelist][variable]})')
        elif (category == 'values_changed'):
            print("Values Changed:")
            for item in diff[category].keys():
                namelist, variable = parse_item(item)
                print(f'  (C)  {namelist} > {variable}: {nml1[namelist][variable]} => ' + 
                        str(nml2[namelist][variable]))
        elif (category == 'type_changes'):
            print("Types Changed:")
            for item in diff[category].keys():
                namelist, variable = parse_item(item)
                print(f'  (T)  {namelist} > {variable}: {nml1[namelist][variable]} => ' + 
                        str(nml2[namelist][variable]))
        else:
            print(f'Category: {category}')
            print(f'Contents: {diff[category]}')

if __name__ == '__main__':
    main()
