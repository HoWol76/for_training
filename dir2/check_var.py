#!/usr/bin/python 
#!/usr/bin/python 

import sys
import os
import re
import shutil
import optparse


def instrument(variable, condition, file_in, file_out, file_name):
    """
    Read in the file line by line looking for assignment to the variable. As we
    go we write lines to an output file. 
    """

    code_added = []
    line_no = 0

    def write_condition(line, args, line_no):
        """
        Check whether the last non-whitespace character on line is a &, if not
        then write out the condition, otherwise skip. Returns whether or not
        anything was written.
        """
        line = line.rstrip()
        if line[-1] == '&':
            return False
        else:
            if args == None:
                print 'Problem at %s#%s' % (file_name, line_no)
            assert(args != None)
            c = condition.replace('%s', variable + args)
            file_out.write(
"""if (%s) then
    print*, 'WARNING: variable condition triggered at %s:%s'
end if\n""" % (c, file_name, line_no))
            return True

    #regex = re.compile('\W%s[ ]*(\(([ ]*\w+[ ]*,?[ ]*)+\))?[ ]*=[^=]' % variable, re.IGNORECASE)
    # Match an assignment to variable, use a simplified regex, the above can be slow (?)
    regex = re.compile('\W%s[ ]*(\([ \w,]+\))?[ ]*=[^=>]' % variable, re.IGNORECASE)

    adding_code = False
    args = None
    for line in file_in:
        line_no = line_no + 1
        file_out.write(line)

        try:
            if line.lstrip()[0] == '!':
                continue
        except IndexError:
                continue

        m = regex.search(line) 
        if m is not None:
            args = m.group(1)

        if m is not None or adding_code:
            wrote = write_condition(line, args, line_no + 2) 
            adding_code = not wrote    
            if wrote:
                code_added.append('dbreak -g %s#%s' % (file_name, line_no + 2))
                line_no = line_no + 3

    return code_added


def main():

    parser = optparse.OptionParser('usage: %prog [options] [variable name] [condition] [Fortran source file name]')
    parser.add_option('-r', '--reverse', help= \
"""Reverse changes made by a previous invokation of this program.
   This just restores a backed up copy of the input file.""")
    (opts, args) = parser.parse_args()

    if opts.reverse is not None:
        try:
            shutil.move('%s.bkp' % opts.reverse, opts.reverse)
        except IOError:
            return 1
        return 0

    if len(args) != 3:
        parser.print_help()
        return 1

    try:
        file_in = open(args[2])
    except Error:
        sys.stderr.write('Could not open input file %s\n' % args[2])
        parser.print_help()
        return 1

    file_out_name = args[2] + '.tmp'
    
    if os.path.exists(file_out_name):
        sys.stderr.write('Temporary file %s.tmp already exists\n' % args[2])
        parser.print_help()
        return 1
        
    try:
        file_out = open(file_out_name, 'w')
    except IOError:
        sys.stderr.write('Could not open output file %s\n' % file_out_name)
        return 1

    code_added = instrument(args[0], args[1], file_in, file_out, args[2])

    file_in.close()
    file_out.close()

    # Make a backup of the original if one does not alread exist. Swap file_in
    # and file_out. 
    if code_added != []:
        if not os.path.exists(args[2] + '.bkp'):
            shutil.move(args[2], args[2] + '.bkp')
        shutil.move(file_out_name, args[2])
        for br in code_added:
            print br
    else:
        os.remove(file_out_name)

    return 0

if __name__ == "__main__":
    sys.exit(main())
