#!/usr/bin/python3

import sys

arguments = sys.argv[1:]

options = {
        "--input" : "",
        "--output" : "",
        "--operation" : "",
        "--trim-right" : "",
        "--trim-left" : ""
}

#Loop to assign the argument to each option
for key in options:
    if key in arguments:
        print(key)
        options[key] = arguments[arguments.index(key)+1]
        print((options[key])

""" Considerations:
              1. Values for trim-right and trim-left must be numerical
              2. If no argument is provided after an option (i.e --input --output) an error should pop up
              3. If operation is not trim. Trim-right and left should not beprovided. Prompt usage message or say that arguments were ignored
              4. two arguments to the same option should prompt an error. All the options (--) will be even indexes (so then all even indexes should have the -- (prompt error or ignore depending on the option) """



