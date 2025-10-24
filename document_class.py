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

    def get_sequence(self):
        return self.sequence

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



#main()

#OPEN FILE AND CREATE RECORD
records = []

with open('insects.fasta', 'rt') as file:
    line_no = 0
    for line in file:
        line_no+=1
        line = line.strip()

        if line_no % 2 == 1:
            header = line
        elif (line_no % 2 == 0):
            sequence = line
            record = Record(header, sequence)
            records.append(record)


print(records[0].get_sequence())
#print(records[0].rc().get_sequence())


#print(records[0].trim().get_sequence())

print(records[0].trim(200,20).get_sequence())


# MODIFY RECORD
#for rec in records:
    #print(len(rec))
    
# rec.reverse... trim... adaptor


#WRITE OUTPUT FILE

#summary()



