"""命令行参数解析模块"""

import argparse  #命令行解析工具
import sys
from ..version import __version__, __description__


def parse_arguments():
    """
    解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -i genome1.fasta genome2.fasta -k 31 -s 0.01
  %(prog)s -l genomes.txt -k 21 -s 0.001 -o results.csv
  %(prog)s -i genome1.fastq genome2.fastq --threads 4 --ani
        """
    )
    
    # 输入方式选择组
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-i', '--input',
        nargs='+',
        help='输入比对的基因组文件，至少两个（空格分隔）'
    )
    input_group.add_argument(
        '-l', '--list',
        help='包含基因组文件路径的列表文件（每行一个文件路径）'
    )
    
    # 核心算法参数
    parser.add_argument(
        '-k', '--kmer-size',
        type=int,
        default=31,
        help='k-mer长度，取值范围[1-64]，默认31'
    )
    parser.add_argument(
        '-s', '--scaled',
        type=float,
        default=0.01,
        help='FracMinHash采样率，取值范围(0,1]，默认0.01'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='哈希函数随机种子，默认42'
    )
    
    # 输出选项
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（默认输出到控制台）'
    )
    parser.add_argument(
        '--format',
        choices=['table', 'json', 'csv'],
        default='table',
        help='输出格式，默认table'
    )
    
    # 计算选项
    parser.add_argument(
        '--ani',
        action='store_true',
        help='计算ANI值（默认只计算Jaccard指数）'
    )
    parser.add_argument(
        '-t','--threads',
        type=int,
        default=1,
        help='并行计算线程数，默认单线程'
    )
    parser.add_argument(
        '-m','--min-similarity',
        type=float,
        default=0.01,
        help='最小相似度阈值，只输出大于该值的结果，默认0.01'
    )
    
    # 其他选项
    parser.add_argument(
        '-v','--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='版本信息'
    )
    parser.add_argument(
        '-V','--verbose',
        action='store_true',
        help='输出详细信息'
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 参数验证
    if args.kmer_size < 1 or args.kmer_size > 64:
        parser.error("k-mer长度必须在1-64之间")
    
    if args.scaled <= 0 or args.scaled > 1:
        parser.error("采样率必须在(0,1]范围内")
    
    if args.min_similarity < 0 or args.min_similarity > 1:
        parser.error("最小相似度必须在0-1之间")
    
    return args