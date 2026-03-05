"""文件读取器模块"""

import os   #文件路径和存在性检查
import sys  #错误输出
from typing import List, Generator, Optional   #类型提示
from .parser.fasta_parser import FastaParser   #导入两个解析器
from .parser.fastq_parser import FastqParser


class FileReader:
    """文件读取器类"""
    
    def __init__(self, verbose=False):
        """
        初始化文件读取器
        
        Args:
            verbose: 是否输出详细信息
        """
        self.verbose = verbose
        self.fasta_parser = FastaParser()
        self.fastq_parser = FastqParser()
    
    def get_file_list(self, input_files: List[str], list_file: Optional[str] = None) -> List[str]:
        """
        获取所有需要处理的文件列表
        
        Args:
            input_files: 直接输入的文件
            list_file: 包含文件路径的列表文件
            
        Returns:
            List[str]: 文件路径列表
        """
        file_list = []
        
        if input_files:
            file_list.extend(input_files)
        
        if list_file:
            try:
                with open(list_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            file_list.append(line)
            except Exception as e:
                sys.stderr.write(f"读取列表文件失败 {list_file}: {e}\n")
                sys.exit(1)
        
        # 验证文件存在性
        valid_files = []
        for file_path in file_list:
            if os.path.exists(file_path):
                valid_files.append(file_path)
            else:
                sys.stderr.write(f"警告: 文件不存在 {file_path}\n")
        
        if not valid_files:
            sys.stderr.write("错误: 没有有效的输入文件\n")
            sys.exit(1)
        
        if self.verbose:
            sys.stderr.write(f"找到 {len(valid_files)} 个有效文件\n")
        
        return valid_files
    
    def read_sequences(self, file_path: str) -> Generator[tuple, None, None]:
        """
        读取文件中的序列
        
        Args:
            file_path: 文件路径
            
        Yields:
            tuple: (序列ID, 序列字符串, 质量分数(仅FASTQ))
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext in ['.fasta', '.fa', '.fna', '.ffn', '.frn']:
                yield from self.fasta_parser.parse(file_path)
            elif file_ext in ['.fastq', '.fq']:
                yield from self.fastq_parser.parse(file_path)
            else:
                # 尝试自动检测格式
                yield from self._auto_detect_parser(file_path)
        except Exception as e:
            sys.stderr.write(f"读取文件失败 {file_path}: {e}\n")
    
    def _auto_detect_parser(self, file_path: str) -> Generator[tuple, None, None]:
        """
        自动检测文件格式并解析
        
        Args:
            file_path: 文件路径
            
        Yields:
            tuple: (序列ID, 序列字符串, 质量分数)
        """
        with open(file_path, 'r') as f:
            first_char = f.read(1)
            f.seek(0)
            
            if first_char == '>':
                yield from self.fasta_parser.parse(file_path)
            elif first_char == '@':
                yield from self.fastq_parser.parse(file_path)
            else:
                raise ValueError(f"无法识别的文件格式: {file_path}")