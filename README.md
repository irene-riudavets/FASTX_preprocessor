# FASTX preprocessor

A small command-line tool written in Python to preprocess **FASTA** and **FASTQ** files. It can reverse-complement sequences, trim bases from either end, and remove a 5' adaptor.

Developed for *Module I: Programming in Bioinformatics* (MSc in Bioinformatics, Universitat Autònoma de Barcelona) by Irene Riudavets Marí and Ferran Jornet Margalef.

## Features

| Operation | What it does |
|---|---|
| `rc` | Reverse complement of every sequence. For FASTQ, the quality string is reversed too, so it stays aligned. |
| `trim` | Hard-trims a fixed number of bases from the left and/or right of every read. Quality strings are trimmed accordingly. |
| `adaptor-removal` | Removes a given adaptor if a read starts with it. |

After each run, a summary is printed: number of reads, number of bases, nucleotide composition (% A, C, G, T, N) and, where relevant, the number of bases trimmed or adaptors found.

## Requirements

- Python: Version 3.13.1 or higher

## Installation

```bash
git clone https://github.com/irene-riudavets/FASTX_preprocessor.git
cd FASTX_preprocessor
chmod +x fastx_pp.py
```

## Usage

```bash
./fastx_pp.py --input <file.fasta|file.fastq> --output <file> --operation <rc|trim|adaptor-removal> [operation options]
```

Run without arguments to see the short usage, or with `-h`, `-help` or `--help` to list all commands.

| Command | Required | Description |
|---|---|---|
| `--input` | yes | Input file, must end in `.fasta` or `.fastq` |
| `--output` | yes | Output file name (same format as the input) |
| `--operation` | yes | `rc`, `trim` or `adaptor-removal` |
| `--adaptor` | with `adaptor-removal` | Adaptor sequence (A, C, G, T, N; case-insensitive) |
| `--trim-left` | with `trim` (at least one of the two) | Positive integer: bases to remove from the left |
| `--trim-right` | with `trim` (at least one of the two) | Positive integer: bases to remove from the right |

Commands can be given in any order. Each command can only be used once.

## Examples

The `examples/` folder contains small test files.

**Reverse complement**

```bash
./fastx_pp.py --input examples/tutorial.fasta --output tutorial_rc.fasta --operation rc
```

**Trim 5 bases from each end**

```bash
./fastx_pp.py --input examples/tutorial.fasta --output tutorial_trimmed.fasta \
              --operation trim --trim-left 5 --trim-right 5
```

**Remove the adaptor `TATAGA`**

```bash
./fastx_pp.py --input examples/tutorial.fasta --output tutorial_tataga_removed.fasta \
              --operation adaptor-removal --adaptor tataga
```

Expected summary:

```
Summary:
3       reads processed
449 bases processed (38.53% A, 9.13% C, 11.36% G, 40.98% T, 0.0% N)
2       adaptors-found
```

The same operations work on FASTQ files:

```bash
./fastx_pp.py --input examples/tutorial.fastq --output tutorial_trimmed.fastq \
              --operation trim --trim-left 5 --trim-right 10
```

More screenshots (FASTA, FASTQ and a 10,000-read dataset) are in the [report](docs/FASTX_PREPROCESSOR.pdf).

## Error handling

The script prints a `WARNING` and exits when:

- `--input`, `--output` or `--operation` is missing
- `--adaptor` is missing with `adaptor-removal`, or contains characters other than A, C, G, T, N
- `--trim-left` / `--trim-right` is missing with `trim`, is not a positive integer, or the total trim is longer than a sequence
- the input file does not exist, or is not `.fasta` / `.fastq`, or its header does not start with `>` / `@`
- a command is repeated, or a command has no argument
- an argument starts with `--`

## How it works

`main()` runs this pipeline:

1. `define_options()` parses the command line
2. `validate_arguments()` checks the options
3. `file_format()` detects FASTA or FASTQ
4. `read_file_input()` builds a list of `Record` objects
5. `operation()` applies `rc`, `trim` or `adaptor-removal`
6. `write_output()` writes the result in the input format
7. `summary()` prints statistics

Each sequence is stored in a `Record` class (header, sequence, quality, original length and trimmed bases).


## Authors

- Irene Riudavets Marí
- Ferran Jornet Margalef

## License

Distributed under the MIT License. See `LICENSE`.
