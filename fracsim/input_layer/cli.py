"""命令行参数解析模块"""

import argparse  #命令行解析工具
from ..version import __version__, __description__


def parse_arguments():
    """
    解析命令行参数

    Returns:
        argparse.Namespace: 解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        usage="%(prog)s [-h] (-i INPUT [INPUT ...] | -l LIST) [options]",
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,  #控制帮助信息的格式
        epilog="""
Examples:
  %(prog)s -i genome1.fasta genome2.fasta -k 21 -s 0.01 
  %(prog)s -l genomes.txt -k 21 -s 0.001 -o output_dir/results.csv
  %(prog)s -i genome1.fastq.gz genome2.fastq.gz --threads 4 --ani -V
        """
    )
    
    # 数据输入方式参数
    input_group = parser.add_mutually_exclusive_group(required=True)  #创建互斥参数组，必须从该组中选择一个参数使用
    input_group.add_argument(
        '-i', '--input',
        nargs='+',  #可接收多个值
        help='Input genome file(s) in FASTA/FASTQ format. Multiple files separated by spaces.'
    )
    input_group.add_argument(
        '-l', '--list',
        help='Input genome file list from a text file (one file path per line).'
    )
    

    # 核心算法参数（K值、采样率、随机数种子）
    parser.add_argument(
        '-k', '--kmer-size',
        type=int,
        default=16,
        help='k‑mer length. Must be an integer between 1 and 64. Default: 16.'
    )
    parser.add_argument(
        '-s', '--scaled',
        type=float,
        default=0.01,
        help='FracMinHash sampling rate. A float in the range (0,1]. Default: 0.01.'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for hash function. Default: 42.'
    )
    

# 计算选项
    parser.add_argument(
        '-a','--ani',
        action='store_true',
        help='Compute Average Nucleotide Identity (ANI) in addition to Jaccard index.'
    )
    parser.add_argument(
        '-t','--threads',
        type=int,
        default=1,
        help='Number of parallel processes. Default: 1.'
    )
    parser.add_argument(
        '-m','--min-similarity',
        type=float,
        default=0.00,
        help='Minimum similarity threshold (Jaccard index, or ANI if --ani is set). Default: 0.0.'
    )


    # 输出选项参数
    parser.add_argument(
        '-o', '--output',
        help='Output file path. If not specified, results are printed to stdout.'
    )
    parser.add_argument(
        '-f','--format',
        choices=['table', 'json', 'csv', 'tsv'],
        default='table',
        help='Output format. Choices: table, json, csv, tsv. Default: table.'
    )
    
    # 内存监测参数
    parser.add_argument(
        '-p','--performance',
        action='store_true',
        help='Enable performance monitoring (total time and peak memory) - high self overhead, may slow down computation.')
    
    # 版本信息，输出过程信息
    parser.add_argument(
        '-v','--version',
        action='version',
        version=f'FracSim {__version__}',
        help='Display program version and exit.'
    )
    parser.add_argument(
        '-V','--verbose',
        action='store_true',
        help='Output detailed information'
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 参数验证
    if args.kmer_size < 1 or args.kmer_size > 64:
        parser.error("k-mer长度必须在1-64之间")
    
    if args.scaled <= 0 or args.scaled > 1:
        parser.error("采样率必须在(0,1]范围内")
    
    if args.min_similarity < 0 or args.min_similarity > 100:
        parser.error("最小相似度必须在0-100之间")
    
    return args