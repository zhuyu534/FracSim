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
        help='从基因组文件输入，多个文件之间使用空格分隔'
    )
    input_group.add_argument(
        '-l', '--list',
        help='从包含基因组文件路径的列表文件输入（每行一个文件路径）'
    )
    

    # 核心算法参数（K值、采样率、随机数种子）
    parser.add_argument(
        '-k', '--kmer-size',
        type=int,
        default=21,
        help='k-mer长度，取值范围[1-64]，默认值21'
    )
    parser.add_argument(
        '-s', '--scaled',
        type=float,
        default=0.01,
        help='FracMinHash采样率，取值范围(0,1]，默认值0.01'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='哈希函数随机种子，默认值42'
    )
    

# 计算选项
    parser.add_argument(
        '-a','--ani',
        action='store_true',
        help='计算输出ANI值（默认只计算Jaccard指数）'
    )
    parser.add_argument(
        '-t','--threads',
        type=int,
        default=1,
        help='计算线程数，默认值1'
    )
    parser.add_argument(
        '-m','--min-similarity',
        type=float,
        default=0.00,
        help='最小相似度阈值，只输出大于该值的结果，默认0.0'
    )


    # 输出选项参数
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径'
    )
    parser.add_argument(
        '-f','--format',
        choices=['table', 'json', 'csv'],
        default='table',
        help='结果输出格式，默认表格格式'
    )
    
    
    # 版本信息，输出过程信息
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