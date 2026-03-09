"""FASTA文件解析器模块"""

import sys  # 标准错误输出
from typing import Generator, Tuple, Union, IO


class FastaParser:
    """FASTA文件解析器类"""
    
    def parse(self, input_source: Union[str, IO]) -> Generator[Tuple[str, str, None], None, None]:
        """
        解析FASTA格式数据
        
        Args:
            input_source: 文件路径（str）或已打开的文本文件对象（IO）
            
        Yields:
            Tuple[str, str, None]: (序列ID, 序列, None)
            
        Raises:
            ValueError: 文件格式错误
        """

        # 根据输入类型打开文件
        if isinstance(input_source, str):
            f = open(input_source, 'r')
            need_close = True
        else:
            f = input_source
            need_close = False

        seq_id = None
        seq_lines = []
        line_num = 0
        
        try:
            for line in f:
                line_num += 1
                line = line.strip()                   
                if not line:  # 跳过空行
                    continue
            
                if line.startswith('>'):  
                    if seq_id is not None and seq_lines:  # 如果之前有序列，先yield
                        sequence = ''.join(seq_lines).upper()
                        yield (seq_id, sequence, None)
                        seq_lines = []
                        
                    # 解析新序列的ID
                    parts = line[1:].split(None, 1)
                    seq_id = parts[0] if parts else f"seq_{line_num}"
                    
                elif seq_id is not None:
                    # 验证序列字符
                    if not self._validate_sequence(line):
                        sys.stderr.write(f"警告: 序列包含非标准字符，行 {line_num}\n")
                    seq_lines.append(line)
                    
                else:
                    raise ValueError(f"FASTA格式错误: 行 {line_num} 在序列标识符之前")
                
            # 处理最后一条序列
            if seq_id is not None and seq_lines:
                sequence = ''.join(seq_lines).upper()
                yield (seq_id, sequence, None)
        
        finally:
            if need_close:
                f.close()
        
    def _validate_sequence(self, seq: str) -> bool:
        """
        验证序列字符是否有效
        
        Args:
            seq: 序列字符串
            
        Returns:
            bool: 是否有效
        """
        valid_chars = set('ATCGUNRYSWKMBDHVatcgunryswkmbdhv')  # 哈希集合检测，标准碱基 + 模糊码
        return all(c in valid_chars for c in seq)
    

