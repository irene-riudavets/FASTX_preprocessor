#!/usr/bin/python3

"""
FASTX Preprocessor Module

This module provides tools to process FASTA/FASTQ files by performing
operations such as reverse complementation, trimming, and adaptor removal. 
It defines a 'Record' class to represent sequence records and command-line
utilities for file parsing and processing.
"""

import sys
import re

class Record:
    """
    Represents a FASTA or FASTQ record.

    A Record object stores a sequence entry, including its identifier,
    nucleotide sequence, and quality (for FASTQ). It also provides
    methods for trimming, reverse-complementing, and adaptor removal.

    Attributes:
        header (str)      :     Sequence identifier (header line).
        sequence (str)    :     Nucleotide sequence.
        quality (str)     :     Quality string (only used for FASTQ records).
        i_length (int)    :     Original sequence length before modification.
        left_out (str)    :     Bases trimmed from the left end.
        right_out (str)   :     Bases trimmed from the right end.
    """

    def __init__(self, header, sequence, quality = ''):
        """
        Initialize a Record instance.

        Args:
            header (str)    : Sequence identifier.
            sequence (str)  : Sequence string.
            quality (str)   : Quality string (for FASTQ).
        """
        
        self.header = header
        self.sequence = sequence
        self.quality = quality
        self.i_length = len(sequence)
        self.left_out= ''
        self.right_out= ''

    def __len__(self):
        """ Return length of the sequence """
        return len(self.sequence)

    def get_header(self):
        """ Return the header."""
        return self.header

    def get_sequence(self):
        """ Return the sequence."""
        return self.sequence
    
    def get_quality(self):
        """ Return the quality string (for FASTQ records)."""
        return self.quality

    def get_i_length(self):
        """Return the original sequence length before Record modification."""
        return self.i_length

    def get_trimmed_bases(self):
        """Return concatenated trimmed bases from both ends."""
        return str(self.left_out+self.right_out)

    def rc(self):
        """
        Compute the reverse complement of the sequence.
        
        The sequence is reversed and complemented. If the input file is FASTQ
        ('f_f == 4'), the quality string is also reversed.
        
        Returns:
            The modified record after reverse complementation.
        """

        self.sequence = self.sequence[::-1].strip().upper().replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper()
        if f_f == 4: #case of a fastq input file
            self.quality = self.quality[::-1]
        return self

    def trim(self, cut_left = 0, cut_right = 0):
        """
        Trim bases from the left and/or right sides of the sequence.
        
        Removes a specified number of bases from the start and/or
        end of the sequence. If the input file is FASTQ ('f_f == 4'),
        the quality scores are trimmed accordingly. 

        Args:
        cut_left (int): Number of bases to trim from the left side.
        cut_right (int): Number of bases to trim from the right side.

        Returns:
            Record: The modified record after trimming.

        Raises:
            SystemExit: If total trim length is greater than sequence length.
        """

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
                sys.exit(f"WARNING. Trim length {l+r} is longer than the sequence length: {len(self)} bp")
            else:
                if options["--operation"] == "adaptor-removal":
                    sys.exit(f"WARNING. Adaptor length {l+r} is longer than the sequence {len(self)}")

    def adaptor(self):
        """
        Detect and remove an adaptor from the beginning of the sequence.
        
        If the sequence starts with the adaptor specified in the
        command-line options, the adaptor length is trimmed from
        the left side of the sequence by calling `self.trim()`.
        
        Returns:
            The modified record after adaptor removal, if adaptor is found.
        """

        if re.match(options["--adaptor"].upper(),self.sequence.upper()):
            return self.trim(len(options["--adaptor"]))

def define_options():
    """Define and parse command-line options.

    Initializes valid command-line arguments and checks their structure.
    Populates the 'options' dictionary with values.

    Raises:
        SystemExit: If argument usage is invalid or required arguments are missing.
    """

    global options
    global commands
    global arguments

    commands = {
            '--help (-h or -help )'   :       'Print available commands',  
            '--input'                 :       'Provide a valid file in .fasta or .fastq format',
            '--operation'             :       {
                '<adaptor-removal>'   :       {
                    '--adaptor'       :        'Search for the provided adaptor sequence and remove it'
                },   
                '<rc>'                :       'Compute the reverse complement of each sequence',
                '<trim>'              :       {
                    '--trim-left'     :       'Trim the specified number of bases starting from the left',
                    '--trim-right'    :       'Trim the specified number of bases starting form the right'
                    }
                },
            '--output'                :       'Provide a name for the created file with the same format as the input file(.fasta or .fastq)'
        }
    options = {
            "--input" : "",
            "--output" : "",
            "--operation" : "", 
            "--trim-right" : 0,
            "--trim-left" : 0,
            "--adaptor" : ""
        }
    
        
    if len(sys.argv)==1 or sys.argv[1] in ['-h', '-help', '--help']:
        print_usage_and_exit()
    
    arguments = sys.argv[1:]
    #Loop to assign the argument to each option
    for i in range(0,len(arguments)):
        if i%2==1 and re.match("--",arguments[i]):
            sys.exit(f'WARNING. Usage <--command> <argument>. Arguments cannot start with \"--\"')    
        elif i%2==0 and not re.match("--",arguments[i]):
            sys.exit(f'WARNING. Usage <--command> <argument>.')

    for key in options:
        if key in arguments:
            try:
                    options[key] = arguments[arguments.index(key)+1]
            except IndexError as ie:
                sys.exit(f'WARNING. No argument was provided for {key}')

def print_usage_and_exit():
    """ Displays available command-line options with usage guidance and terminates execution."""
    
    print('Usage: ./fastx_pp.py --command(s) <argument(s)>')
    if len(sys.argv) != 1:
        print('\nAvailable commands:\n')
        print_commands(commands)
    elif len(sys.argv) == 1:
        print('To see available commands use: -h, -help or --help')
    sys.exit()

def print_commands(commands, indent=0):
    """Print all available commands with indentation.

    Args:
        commands (dict): Dictionary of available command-line options.
        indent (int): Indentation level for nested commands.
    """
    
    for key in sorted(commands):
        value = commands[key]
        if isinstance(value, dict): #The isinstance() function returns True if the specified object is of the specified type, otherwise False.
            print(' ' * indent + f"{key}:")
            print_commands(value, indent + 4)
        else:
            print(' ' * indent + f"{key}: {value}\n")

def validate_arguments(options):
    """Validate command-line arguments.

    Checks that arguments are recognized, properly formatted, and compatible
    with selected operations.

    Args:
        options (dict): Dictionary containing parsed command-line arguments.

    Raises:
        SystemExit: If any validation error or logical conflict is found.
    """

    # 1. Check that all command-line arguments are recognized

    command = re.findall(r'(--\S[^\']+)', str(arguments))
    for i in command:
        if i not in options:
            sys.exit(f'WARNING. Command {i} not recognised.\nUse ./FASTX_processor.py <-h> or <--help> for usage information')
        elif command.count(i)>1:
            sys.exit(f'WARNING. Command {i} is repeated, it must only be provided once')

    # 2. Verify that the required options are provided
    
    if not options["--input"]:    
        sys.exit("WARNING. No input file provided. Use --input <filename>")
    elif not options["--output"]:
        sys.exit("WARNING. No output file provided. Use --output <filename>")
    elif not options["--operation"]:
        sys.exit("WARNING. No operation provided. Use --operation <rc|trim|adaptor-removal>")

    # 3. Valid operation type check
    
    value = str(options["--operation"]).lower()
    if value not in ('rc', 'trim', 'adaptor-removal'):
        sys.exit("WARNING. Provide a valid operation: <rc>, <trim> or <adaptor-removal>")
    
    # 4. Specific operation checks

    if value == 'trim':
        # Both trim-left and trim-right must be positive (or 0) integers
        trim_value = []
        for key in ("--trim-left", "--trim-right"):
            value = str(options[key]) 
            trim_value.append(value)

            if not value.isdigit() or int(value) < 0:
                sys.exit(f"WARNING. {key} must be a positive integer")

        if trim_value.count('0') == 2: # Case where no --trim-left or --trim-right was provided
            sys.exit(f"WARNING. When using --operation trim, provide --trim-left and/or --trim-right followed by a positive integer")

    elif value == 'adaptor-removal':
        # Adapotor sequence cannot be empty and only contain valid characters
        adaptor = options["--adaptor"].upper()
        if not adaptor:
            sys.exit("WARNING. When using --operation adaptor-removal, provide --adaptor <sequence>")
        if not re.fullmatch(r"[ACGTN]+", adaptor):
            sys.exit("WARNING. Adaptor sequence must only contain A, C, G, T or N")

def file_format():
    """Determine the input file type.

    Checks whether the input file is a FASTA or FASTQ file based on
    file extension and header format.

    Returns:
        int: 2 if input is FASTA, 4 if input is FASTQ.

    Raises:
        SystemExit: If the file format is invalid or cannot be read.
    """
    
    try:
        with open(options["--input"],"rt") as file:
            first_line=file.readline()
            if (re.search(r".fasta$",options["--input"])) and (re.match(">", first_line)):
                return 2
            elif (re.search(r".fastq$",options["--input"])) and (re.match("@",first_line)):
                return 4
            else:
                sys.exit("WARNING. Invalid file format. Use only .fasta or .fastq files")
    except FileNotFoundError:
        sys.exit("WARNING. Unable to read input file")

def read_file_input(): #OPEN FILE AND CREATE RECORD
    """Parse input file and load sequence records.

    Reads a FASTA/FASTQ file line by line, constructing Record objects
    for each entry.

    Returns:
        records (list): List of Record objects extracted from the input file.
        It will contain all input file information (header, sequence, <quality>)
    """
    
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
                if f_f==2: # In case of fasta format (f_f = 2) record will only contain header and sequence
                    record = Record(header, sequence) 
                    records.append(record)
            elif line_no % f_f == 3: # only when fastq format (f_f = 4) quality will be included in record
                quality = line
                record = Record(header,sequence,quality)
                records.append(record)
            line_no+=1

def operation():
    """Perform selected sequence operation.

    Applies the operation specified by the user ('rc', 'trim', or 'adaptor-removal')
    to every sequence record. 
    """
    
    for rec in records:
        if options["--operation"] == "rc":
            rec.rc()

        elif options["--operation"] == "trim":
            rec.trim(options["--trim-left"],options["--trim-right"])

        elif options["--operation"] == "adaptor-removal":
            rec.adaptor()
    
    print_message={"rc":"reversed-complemented","trim":"hard-trimmed","adaptor-removal":"processed"}
    print(f'File \'{options["--input"]}\' was succesfully {print_message[options["--operation"]]} (\'{options["--output"]}\')')

def write_output():
    """Write processed records to the output file.

    Writes sequence data to the specified output file in the same format
    as the input (FASTA or FASTQ).
    """
    
    with open(options["--output"],"wt") as fd:
        for rec in records:
            fd.write(rec.get_header()+'\n')
            fd.write(rec.get_sequence()+'\n')
            
            if f_f==4:
                fd.write('+\n')
                fd.write(rec.get_quality()+'\n')

def summary():
    """Print a summary of the input file and results.

    Calculates and prints overall bases processed, number of processed reads,
    and summary statistics depending on the operation performed.
    """

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
            if len(rec) != rec.get_i_length(): #get_i_length return the length of each sequence from the input file
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

def main():
    """Execute the FASTX preprocessing pipeline."""
    
    define_options()
    validate_arguments(options)
    global f_f
    f_f = file_format()
    read_file_input()
    operation()
    write_output()
    summary()
    
main()
