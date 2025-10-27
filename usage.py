#!/usr/bin/python3

import re
import sys

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
    print('\nTo get full help for a command use one of the following:\nFASTX_preprocessor command -h\nFASTX_preprocessor --help\n')
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


def error():
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '-help', '--help']:
        print_usage_and_exit()
    
    command=re.findall(r'(--\S[^\']+)', str(arguments))
    print(command)
    for i in command:
        if i not in options:
            print('Command "' + i + '" not recognised.\n')
            print_usage_and_exit()



options = {
        "--input" : "",
        "--output" : "",
        "--operation" : "", #try to see if multiple values can be set for the same key
        "--trim-right" : "",
        "--trim-left" : "",
        "--adaptor" : ""
}
arguments = sys.argv[1:]



#error()
try: 
    with open("insects.fast:","rt") as f:
        print("abrimos bitch")
        
except:
    print("not work bitch")






#error()

