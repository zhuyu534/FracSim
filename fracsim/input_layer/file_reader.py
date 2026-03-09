"""文件读取器模块"""

import os   # 文件路径和存在性检查
import sys  # 错误输出信息
import gzip
import bz2
import lzma
import zipfile
import io
from typing import List, Generator, Optional,Tuple   # 类型提示
from .parser.fasta_parser import FastaParser   # 导入两个解析器
from .parser.fastq_parser import FastqParser
from ..process_layer.models import GenomeData  # 导入 GenomeData 类

class FileReader:
    """文件读取器类(支持压缩格式)"""
    
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
    

    # --------检测压缩类型---------
    def _detect_compression(self, file_path: str) -> Tuple[Optional[str], str]:
        """
        检测文件是否为压缩格式，并返回 (压缩类型, 实际扩展名)
        压缩类型: None, 'gz', 'bz2', 'xz', 'zip'
        """
        COMPRESS_EXTS = {'.gz': 'gz', '.bz2': 'bz2', '.xz': 'xz', '.zip': 'zip'}
        ext = os.path.splitext(file_path)[1].lower()
        if ext in COMPRESS_EXTS:
            compression = COMPRESS_EXTS[ext]
            # 去掉压缩后缀，再取一次扩展名作为实际格式
            base_path = file_path[: -len(ext)]
            base_ext = os.path.splitext(base_path)[1].lower()
        else:
            compression = None
            base_ext = ext
        return compression, base_ext

    # ----------解压到内存----------
    def _decompress_to_memory(self, file_path: str, compression: str) -> io.TextIOBase:
        """
        将压缩文件解压到内存，返回一个文本文件对象
        支持 gz, bz2, xz, zip
        """
        mem_buffer = io.BytesIO()

        try:
            if compression == 'gz':
                with gzip.open(file_path, 'rb') as src:
                    while chunk := src.read(8192):
                        mem_buffer.write(chunk)
            elif compression == 'bz2':
                with bz2.open(file_path, 'rb') as src:
                    while chunk := src.read(8192):
                        mem_buffer.write(chunk)
            elif compression == 'xz':
                with lzma.open(file_path, 'rb') as src:
                    while chunk := src.read(8192):
                        mem_buffer.write(chunk)
            elif compression == 'zip':
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    # 取第一个非目录文件
                    for name in zipf.namelist():
                        if not name.endswith('/'):
                            with zipf.open(name, 'r') as src:
                                while chunk := src.read(8192):
                                    mem_buffer.write(chunk)
                            break
                    else:
                        raise ValueError(f"ZIP文件中没有可读取的文件: {file_path}")
            else:
                raise ValueError(f"不支持的压缩格式: {compression}")
        except Exception as e:
            raise IOError(f"解压文件失败 {file_path}: {e}")

        mem_buffer.seek(0)
        # 将二进制流包装为文本流（解析器需要文本模式）
        text_stream = io.TextIOWrapper(mem_buffer, encoding='utf-8')
        # 保留 buffer 引用，防止被垃圾回收
        text_stream._buffer = mem_buffer
        return text_stream

    
    def read_sequences(self, file_path: str) -> Generator[tuple, None, None]:  # 序列读取接口，根据文件类型分配解析器
        """
        读取文件中的序列，支持普通文件及压缩格式（.gz/.bz2/.xz/.zip）
        压缩文件将解压到内存后由解析器处理

        Yields:
            tuple: (序列ID, 序列字符串, 质量分数)
        """
        compression, base_ext = self._detect_compression(file_path)

        try:
            # 根据实际格式分发
            if base_ext in ['.fasta', '.fa', '.fna', '.ffn', '.frn']:
                if compression:
                    # 压缩文件：解压到内存再解析
                    mem_file = self._decompress_to_memory(file_path, compression)
                    yield from self.fasta_parser.parse(mem_file)
                else:
                    yield from self.fasta_parser.parse(file_path)

            elif base_ext in ['.fastq', '.fq']:
                if compression:
                    mem_file = self._decompress_to_memory(file_path, compression)
                    yield from self.fastq_parser.parse(mem_file)
                else:
                    yield from self.fastq_parser.parse(file_path)

            else:
                # 未知扩展名，尝试自动检测（可能为压缩文件）
                yield from self._auto_detect_parser(file_path, compression)

        except Exception as e:
            sys.stderr.write(f"读取文件失败 {file_path}: {e}\n")

    #----------自动检测格式 ----------
    def _auto_detect_parser(self, file_path: str, compression: Optional[str] = None) -> Generator[tuple, None, None]:
        """
        自动检测文件格式并解析（支持压缩文件）
        """
        try:
            # 如果是压缩文件，先解压到内存
            if compression:
                mem_file = self._decompress_to_memory(file_path, compression)
                # 递归调用自身，此时 compression=None，mem_file 作为文件对象
                yield from self._auto_detect_parser(mem_file, compression=None)
                return

            # 此时 file_path 可能是普通路径或内存文件对象
            if isinstance(file_path, io.TextIOBase):
                f = file_path
                need_rewind = True
            else:
                f = open(file_path, 'r')
                need_rewind = False

            with f:
                # 读取第一个非空字符
                first_char = None
                for line in f:
                    line = line.strip()
                    if line:
                        first_char = line[0]
                        break
                if not first_char:
                    raise ValueError("文件为空")

                f.seek(0)  # 重置指针

                if first_char == '>':
                    if isinstance(file_path, io.TextIOBase):
                        yield from self.fasta_parser.parse(f)
                    else:
                        yield from self.fasta_parser.parse(file_path)
                elif first_char == '@':
                    if isinstance(file_path, io.TextIOBase):
                        yield from self.fastq_parser.parse(f)
                    else:
                        yield from self.fastq_parser.parse(file_path)
                else:
                    raise ValueError(f"无法识别的文件格式，首字符: '{first_char}'")

        except Exception as e:
            raise ValueError(f"自动检测失败: {e}")
        
    def read_genome(self, file_path: str) -> GenomeData:
        """
        读取一个基因组文件的所有序列，返回包含多条序列的 GenomeData 对象
    
        Args:
            file_path: 文件路径
        
        Returns:
            GenomeData: 包含所有序列的基因组数据
        """
        sequences = []
        genome_id = os.path.basename(file_path)  # 使用文件名作为基因组ID
    
        # 读取所有序列
        for _, sequence, _ in self.read_sequences(file_path):
            sequences.append(sequence)
    
        return GenomeData(
            file_path=file_path,
            seq_id=genome_id,
            sequences=sequences  
        )

