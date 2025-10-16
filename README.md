# FASTX_preprocessor

Python tool to process both FASTA and FASTQ files


NOTE: FASTQ files can be converted to FASTA files by using the following command:

sed -n '1~4s/^@/>/p;2~4p' file.fastq > file.fasta


