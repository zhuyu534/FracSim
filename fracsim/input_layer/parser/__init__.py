"""解析器模块"""

from .fasta_parser import FastaParser
from .fastq_parser import FastqParser

__all__ = ['FastaParser', 'FastqParser']