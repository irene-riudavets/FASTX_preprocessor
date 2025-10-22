#!/usr/bin/python3

import sys
import re

arguments = sys.argv[1:]

options = {
        "--input" : "",
        "--output" : "",
        "--operation" : "", #try to see if multiple values can be set for the same key
        "--trim-right" : "",
        "--trim-left" : "",
        "--adaptor" : ""
}

#Loop to assign the argument to each option
for key in options:
    if key in arguments:
        options[key] = arguments[arguments.index(key)+1]
""" Considerations:
              1. Values for trim-right and trim-left must be numerical
              2. If no argument is provided after an option (i.e --input --output) an error should pop up
              3. If operation is not trim. Trim-right and left should not beprovided. Prompt usage message or say that arguments were ignored
              4. two arguments to the same option should prompt an error. All the options (--) will be even indexes (so then all even indexes should have the -- (prompt error or ignore depending on the option) """

#Would be a good idea to add try/except here because if you use something that is not a file, it breaks...

def file_format():
    """ function that checks the format of the input file. 
    Only valid .fasta and .fastq. """
    
    with open(options["--input"],'rt') as file:
        first_line=file.readline()
        if (re.search(r".fasta$",options["--input"])) and (">" in first_line):
            return 2
        
        elif (re.search(r".fastq$",options["--input"])) and ("@" in first_line):
            return 4
        else:
            print("Not a valid file")
            return None
    

#Function to create the summary for the functions

def summary():
    with open(options["--input"],'rt') as file:
        line_no = 0
        reads = 0
        f_f=file_format()
        A = C = G = T = N = 0
        for line in file:
            if (line_no % f_f == 1): 
                line.upper()
                a,c,t,g,n = line.count("A"),line.count("C"),line.count("T"),line.count("G"), line.count("N")
                A+=a;C+=c;T+=t;G+=g;N+=n
                line_no+=1
                reads+=1
            else:
                line_no+=1

        total_bases=A+C+T+G+N
        print(total_bases)
        print("Summary:")
        print(f'{reads}\t reads processed')
        print(f'{str(total_bases)} bases processed ({round(((A/total_bases)*100),1)}% A, {round(((C/total_bases)*100),1)}% C, {round(((G/total_bases)*100),1)}% G, {round(((T/total_bases)*100),1)}% T, {round(((N/total_bases)*100),1)} % N)')



def reverse():
    """ Do the reverse of every sequence in a FASTA file """
    a=file_format()

    if a is None:
        sys.exit("Error: invalid or missing input file.")

    with open(options["--input"], 'rt') as file:
        with open(options["--output"],'wt') as fd:
            line_no=0
            reads=0
            A=C=T=G=N=0
            if a == 2:
                for line in file:
                    line_no += 1
                    if line_no % 2 == 1:
                        fd.write(line)
                    elif line_no % 2 == 0: 
                        rc_line=line[::-1].strip().upper().replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper()
                        fd.write(rc_line+'\n')
            elif a == 4:
                for line in file:
                    line_no += 1
                    module=line_no%4
                    if module == 1:
                        fd.write(line)
                    elif module == 2: 
                        rc_line=line[::-1].strip().upper().replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper()
                        fd.write(rc_line+'\n')
                    elif module == 3: 
                        fd.write(line[::-1].strip()+'\n')
                    elif module == 0:
                        fd.write('\n')

#def adaptor_removal(adaptor):


#Main function here
#reverse()


def main():

    summary()


main()





    
