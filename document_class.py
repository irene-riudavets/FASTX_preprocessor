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
        self.i_length = len(sequence)
        self.left_out= ''
        self.right_out= ''

    #def __repr__(self): #could use __str__ as well
        """ Returns the record as a string """
        #return self.strip()

    def __len__(self):
        """ Return length of the sequence """
        return len(self.sequence)

    def get_header(self):
        return self.header

    def get_sequence(self):
        return self.sequence
    
    def get_quality(self):
        return self.quality
    
    def get_i_length(self):
        return self.i_length

    def get_trimmed_bases(self):
        return str(self.left_out+self.right_out)

    def rc(self):
        """ Reverse complement of the sequence """
        self.sequence = self.sequence[::-1].strip().upper().replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper()
        if f_f == 4: #case of a fastq input file
            self.quality = self.quality[::-1]
        return self


    def trim(self, cut_left = 0, cut_right = 0):
        """ Trim bases """
        l=int(cut_left)
        r=int(cut_right)
        if l+r < len(self):
            self.left_out=self.sequence[0:l:1]
            self.right_out=self.sequence[(len(self)-r)::1]
            self.sequence = self.sequence[l:(len(self)-r):1]


            if f_f == 4:
                self.quality = self.quality[l:((self.i_length)-r):1]
            return self
        else:
            if options["--operation"] == "trim":
                sys.exit(f"Trim length {l+r} is longer than the sequence {len(self)}")
            else:
                if options["--operation"] == "adaptor-removal":
                    sys.exit(f"Adaptor length {l+r} is longer than the sequence {len(self)}")


    def adaptor(self):

        """ Method to find the adaptor sequence within the sequence and
        trim it. This method calls self.trim since it performs the
        operation of removing a certain number of bases """

        if re.match(options["--adaptor"],self.sequence):
            return self.trim(len(options["--adaptor"]))

#FALTAR AFEGIR A UNA FUNCIO------------------------------------------
arguments = sys.argv[1:]

options = {
        "--input" : "",
        "--output" : "",
        "--operation" : "", 
        "--trim-right" : 0,
        "--trim-left" : 0,
        "--adaptor" : ""
}

commands = {
        'input'                 :       'Provide a valid file in .fasta or .fastq format',
        'operation'             :       {
            'adaptor-removal'   :       'Search for the provided adaptor sequence and remove it',   
            'rc'                :       'Compute the reverse complement of each sequence',
            'trim'              :       {
                'trim-left'     :       'Trim the specified number of bases starting from the left',
                'trim-right'    :       'Trim the specified number of bases starting form the right'
                }
            },
        'output'                :       'Provide a name for the created file with the same format as the input file(.fasta or .fastq)'
    }


def print_usage_and_exit():
    print('Usage: FASTX_preprocessor <command> [options]')
    print('\nAvailable commands:\n')
    print_commands(commands)
    sys.exit()


def print_commands(commands, indent=0):
    for key in sorted(commands):
        value = commands[key]
        if isinstance(value, dict): #The isinstance() function returns True if the specified object is of the specified type, otherwise False.
            print(' ' * indent + f"{key}:")
            print_commands(value, indent + 4)
        else:
            print(' ' * indent + f"{key}: {value}\n")


#Loop to assign the argument to each option
for key in options:
    if key in arguments:
        try:
                options[key] = arguments[arguments.index(key)+1]
        
        except IndexError as ie:
            sys.exit(f"No argument was provided for {key}")

def validate_arguments(options):

    # 1. Check that all command-line arguments are recognized

    command = re.findall(r'(--\S[^\']+)', str(arguments))
    for i in command:
        if i not in options:
            sys.exit(f'Command {i} not recognised.\nUse ./FASTX_processor.py <-h> or <--help> for usage information')

    # 2. Verify that the required options are provided
    
    if not options["--input"]:    
        sys.exit("Error: no input file provided. Use --input <filename>")

    if not options["--output"]:
        sys.exit("Error: no output file provided. Use --output <filename>")

    if not options["--operation"]:
        sys.exit("Error: No operation provided. Use --operation <rc|trim|adaptor-removal>")


    # 3. Valid operation type check

    value = str(options["--operation"]).lower()
    if value not in ('rc', 'trim', 'adaptor-removal'):
        sys.exit("Please provide a valid operation: <rc>, <trim> or <adaptor-removal>")
    
    # 4. Specific operation checks

    if value == 'trim':
        # Both trim-left and trim-right must be positive (or 0) integers
        trim_value = []
        for key in ("--trim-left", "--trim-right"):
            value = str(options[key]) 
            trim_value.append(value)

            if not value.isdigit() or int(value) < 0:
                sys.exit(f"{key} must be a positive integer")

        if trim_value.count('0') == 2:
            sys.exit(f"Error: when using --operation trim, provide --trim-left and/or --trim-right followed by a positive integer")

    elif value == 'adaptor-removal':
        # Adapotor sequence cannot be empty and only contain valid characters
        adaptor = options["--adaptor"].upper()
        if not adaptor:
            sys.exit("Error: when using --operation adaptor-removal, provide --adaptor <sequence>")
        if not re.fullmatch(r"[ACGTN]+", adaptor):
            sys.exit("Error: Adaptor sequence must only contain A, C, G, T or N")

#--------------------------------------------------------------------

def file_format():
    """ function that checks the format of the input file.
    Only valid .fasta and .fastq. """
    try:
        with open(options["--input"],"rt") as file:
            first_line=file.readline()
            if (re.search(r".fasta$",options["--input"])) and (re.match(">", first_line)):
                return 2
            elif (re.search(r".fastq$",options["--input"])) and (re.match("@",first_line)):
                return 4
            else:
                sys.exit("Invalid file format. Use only .fasta or .fastq files")
    except FileNotFoundError:
        sys.exit("Unable to read input file")

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
            rec.trim(options["--trim-left"],options["--trim-right"])

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


# Summary ====================================================

def summary():
    """ Print summary statistics for the FASTA/FASTQ file """

    bases = {'A' : 0, 'C' : 0, 'G' : 0, 'T' : 0, 'N' : 0}

    with open(options["--input"],'rt') as file:
        line_no = 0
        for line in file:
            if line_no % f_f == 1:
                for base in bases:
                    bases[base] += line.upper().count(base)
            line_no += 1        

    total_bases = sum(bases.values())
    print("Summary:")
    print(f'{len(records)}\t reads processed')
    
    percentages = {}
    for base in bases:
        percentages[base] = round((bases[base] / total_bases) * 100, 2)
    
    print(f'{total_bases} bases processed '
          f'({percentages['A']}% A, {percentages['C']}% C, '
          f'{percentages['G']}% G, {percentages['T']}% T, '
          f'{percentages['N']}% N)')

    #Extra information for --operation <trim> and <adaptor-removal>
    

    if options["--operation"] == "adaptor-removal":
        num_adaptors = 0
        for rec in records:
            if len(rec) != rec.get_i_length():
                num_adaptors += 1
        print(f'{num_adaptors}\tadaptors-found')
    

    elif options["--operation"] == "trim":
        trim_bases=0
        trim_counts = {'A' : 0, 'C' : 0, 'G' : 0, 'T' : 0, 'N' : 0}

        for rec in records:
            trim_seq = str(rec.get_trimmed_bases().upper()) 
            trim_bases += len(trim_seq)
            for base in trim_counts:
                trim_counts[base] += trim_seq.count(base)
        
        total_trimmed = sum(trim_counts.values())

        percentages_trim = {}
        for base in trim_counts:
            percentages_trim[base] = round((trim_counts[base] / total_trimmed) * 100, 2)
        print(f'{total_trimmed} bases trimmed '
              f'({percentages_trim['A']}% A,' 
              f' {percentages_trim['C']}% C,'
              f' {percentages_trim['G']}% G,'
              f' {percentages_trim['T']}% T,'
              f' {percentages_trim['N']}% N)')

#VARIABLES GLOBALS EN TOT EL CODI: F_F, OPTIONS I RECORDS

 
# MODIFY RECORD
#for rec in records:
    #print(len(rec))
    
# rec.reverse... trim... adaptor

def main():
    global f_f
    try:
        f_f=file_format()
    except FileNotFoundError:
        sys.exit("Unable to read input file")

    read_file_input()
    operation()
    write_output()
    summary()
#WRITE OUTPUT FILE



def proba_main():
    global f_f
    f_f=file_format() #AFEGIR ERROR SI F_F = None
    print(f_f)
    #read_file_input()

#proba_main()

def prova_main():
    if sys.argv[1] in ['-h', '-help', '--help']:
        print_usage_and_exit()

    validate_arguments(options)
    global f_f
    f_f = file_format()
    read_file_input()
    operation()
    write_output()
    summary()


prova_main()

