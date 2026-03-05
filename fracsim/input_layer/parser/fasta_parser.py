"""FASTA文件解析器模块"""

import sys  #用于向标准错误输出警告信息
from typing import Generator, Tuple  


class FastaParser:
    """FASTA文件解析器类"""
    
    def parse(self, file_path: str) -> Generator[Tuple[str, str, None], None, None]:
        """
        解析FASTA文件
        
        Args:
            file_path: FASTA文件路径
            
        Yields:
            Tuple[str, str, None]: (序列ID, 序列字符串, None)
            
        Raises:
            ValueError: 文件格式错误
        """
        seq_id = None
        seq_lines = []
        line_num = 0
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line_num += 1
                    line = line.strip()
                    
                    if not line:  # 跳过空行
                        continue
                    
                    if line.startswith('>'):
                        # 如果之前有序列，先yield
                        if seq_id is not None and seq_lines:
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
        
        except IOError as e:
            raise IOError(f"无法读取文件 {file_path}: {e}")
    
    def _validate_sequence(self, seq: str) -> bool:
        """
        验证序列字符是否有效（仅包含ATCGN）
        
        Args:
            seq: 序列字符串
            
        Returns:
            bool: 是否有效
        """
        valid_chars = set('ATCGUNatcgun')
        return all(c in valid_chars for c in seq)
    

