#!/usr/bin/python3

import sys

arguments = sys.argv[1:]

options = {
        "--input" : "",
        "--output" : "",
        "--operation" : "", #try to see if multiple values can be set for the same key
        "--trim-right" : "",
        "--trim-left" : ""
}

#Loop to assign the argument to each option
for key in options:
    if key in arguments:
        print(key)
        options[key] = arguments[arguments.index(key)+1]
        print((options[key]))              

""" Considerations:
              1. Values for trim-right and trim-left must be numerical
              2. If no argument is provided after an option (i.e --input --output) an error should pop up
              3. If operation is not trim. Trim-right and left should not beprovided. Prompt usage message or say that arguments were ignored
              4. two arguments to the same option should prompt an error. All the options (--) will be even indexes (so then all even indexes should have the -- (prompt error or ignore depending on the option) """



def reverse_FASTA():
    """ Do the reverse of every sequence in a FASTA file """
    with open(options["--input"], 'rt') as file:
        with open("reversed.fasta", 'at') as fd:
            line_no = 0
            for line in file:
                line_no += 1
                if line_no % 2 == 1:
                    fd.write(line)
                elif line_no % 2 == 0:
                    fd.write(line[::-1].strip()+'\n')


reverse_FASTA()








    
