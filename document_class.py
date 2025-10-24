#!/usr/bin/python3

import sys
import re

class Record:
    """ Object representing a FASTX record.

    Attributes:
        header      (str):     Sequence Identifier
        sequence    (str):     Sequence
        quality     (str):     Sequence quality (only for FASTQ)
    """

    def __init__(self, header, sequence, quality = ''):
        self.header = header
        self.sequence = sequence
        self.quality = quality

    #def __repr__(self): #could use __str__ as well
        """ Returns the record as a string """
        #return self.strip()

    def __len__(self):
        """ Return length of the sequence """
        #PROGRAM BASE CONUNTER IN HERE... RETURNS THE LENGTH OF SEQUENCE IF IT ONLY CONTAINS VALID CHARACTERS (A, C, G, T OR N)
        return len(self.sequence)

    def get_header(self):
        return self.header

    def get_sequence(self):
        return self.sequence
    
    def get_quality(self):
        return self.quality

    def rc(self):
        """ Reverse complement of the sequence """
        self.sequence = self.sequence[::-1].strip().upper().replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper()
        return self

    def trim(self, cut_left = 0, cut_right = 0):
        """ Trim bases """
        l=int(cut_left)
        r=int(cut_right)
        if l+r < len(self):
            self.sequence = self.sequence[l:(len(self)-r):1]
            return self
        else:
            sys.exit(f"Trim length {l+r} is longer than the sequence {len(self)}")

    #def adaptor(self):
        #if re.match(options["--adaptor"],self.sequence)
        #call self.trim(len(options["--adaptor"])

#FALTAR AFEGIR A UNA FUNCIO------------------------------------------
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
#--------------------------------------------------------------------

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

def read_file_input(): #OPEN FILE AND CREATE RECORD
    global records 
    records = []
    with open(options["--input"], 'rt') as file:
        line_no = 0
        for line in file:
            line = line.strip()
            if line_no % f_f == 0:
                header = line
            elif line_no % f_f == 1:
                sequence = line
                if f_f==2: #Quan sigui arxiu fasta (f_f=2) nomes afegira header i sequence
                    record = Record(header, sequence) 
                    records.append(record)
            elif line_no % f_f == 3: # en cas de arxiu fastq modul arriba a 3 i s'ha d'afegir la qualitat
                quality = line
                record = Record(header,sequence,quality)
                records.append(record)
            line_no+=1

def operation():
    for rec in records:
        if options["--operation"] == "rc":
            rec.rc()
        elif options["--operation"] == "trim":
            rec.trim()
        elif options["--operation"] == "adaptor-removal":
            rec.adaptor()

def write_output():
    with open(options["--output"],"wt") as fd:
        for rec in records:
            fd.write(rec.get_header()+'\n')
            fd.write(rec.get_sequence()+'\n')
            if f_f==4:
                fd.write('+\n')
                fd.write(rec.get_quality()+'\n')
            
#VARIABLES GLOBALS EN TOT EL CODI: F_F, OPTIONS I RECORDS

 
# MODIFY RECORD
#for rec in records:
    #print(len(rec))
    
# rec.reverse... trim... adaptor

def main():
    f_f=file_format()
    read_file_input()
    operation()
    write_output()
#WRITE OUTPUT FILE

#summary()


def proba_main():
    global f_f
    f_f=file_format() #AFEGIR ERROR SI F_F = None
    print(f_f)
    read_file_input()
    print(len(records))

proba_main()
