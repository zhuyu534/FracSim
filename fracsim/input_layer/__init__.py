"""输入层模块"""

from .cli import parse_arguments
from .file_reader import FileReader
from .parser.fasta_parser import FastaParser
from .parser.fastq_parser import FastqParser

__all__ = [
    'parse_arguments',
    'FileReader',
    'FastaParser',
    'FastqParser'
]