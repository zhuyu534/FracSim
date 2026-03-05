"""FASTQ文件解析器模块"""

import sys
from typing import Generator, Tuple


class FastqParser:
    """FASTQ文件解析器类"""
    
    def parse(self, file_path: str) -> Generator[Tuple[str, str, str], None, None]:
        """
        解析FASTQ文件
        
        Args:
            file_path: FASTQ文件路径
            
        Yields:
            Tuple[str, str, str]: (序列ID, 序列字符串, 质量分数字符串)
            
        Raises:
            ValueError: 文件格式错误
        """
        line_num = 0
        
        try:
            with open(file_path, 'r') as f:
                while True:
                    # 读取ID行
                    seq_id_line = f.readline()
                    line_num += 1
                    if not seq_id_line:
                        break
                    
                    seq_id_line = seq_id_line.strip()
                    if not seq_id_line.startswith('@'):
                        raise ValueError(f"FASTQ格式错误: 行 {line_num} 应以@开头")
                    
                    parts = seq_id_line[1:].split(None, 1)
                    seq_id = parts[0] if parts else f"seq_{line_num}"
                    
                    # 读取序列行
                    sequence_line = f.readline().strip()
                    line_num += 1
                    if not sequence_line:
                        raise ValueError(f"FASTQ格式错误: 行 {line_num} 缺少序列")
                    
                    if not self._validate_sequence(sequence_line):
                        # 找出非法字符位置
                        invalid_chars = self._find_invalid_chars(sequence_line)
                        sys.stderr.write(
                            f"警告: 序列包含非标准字符，行 {line_num}，"
                            f"位置: {invalid_chars}\n"
                        )
                    sequence = sequence_line.upper()
                    
                    # 读取分隔行
                    sep_line = f.readline().strip()
                    line_num += 1
                    if not sep_line.startswith('+'):
                        raise ValueError(f"FASTQ格式错误: 行 {line_num} 应以+开头")
                    
                    # 读取质量行
                    quality_line = f.readline().strip()
                    line_num += 1
                    if not quality_line:
                        raise ValueError(f"FASTQ格式错误: 行 {line_num} 缺少质量分数")
                    
                    quality = quality_line
                    
                    # 验证序列和质量长度一致
                    if len(sequence) != len(quality):
                        raise ValueError(f"FASTQ格式错误: 序列长度({len(sequence)})与质量长度({len(quality)})不一致")
                    
                    yield (seq_id, sequence, quality)
        
        except IOError as e:
            raise IOError(f"无法读取文件 {file_path}: {e}")
        

    def _validate_sequence(self, seq: str) -> bool:
        """
        验证序列字符是否有效（支持ATCGUN，大小写不敏感）
        
        Args:
            seq: 序列字符串
            
        Returns:
            bool: 是否所有字符都有效
        """
        valid_chars = set('ATCGUNatcgun')
        return all(c in valid_chars for c in seq)
    

    def _find_invalid_chars(self, seq: str) -> str:
        """
        找出序列中的非法字符及其位置
        
        Args:
            seq: 序列字符串
            
        Returns:
            str: 描述非法字符的位置信息
        """
        valid_chars = set('ATCGUNatcgun')
        invalid_positions = []
        invalid_chars_found = set()
        
        for i, c in enumerate(seq, 1):  
            if c not in valid_chars:
                invalid_positions.append(str(i))
                invalid_chars_found.add(c)
        
        if invalid_positions:
            return f"位置: {', '.join(invalid_positions)}，非法字符: {', '.join(invalid_chars_found)}"
        return "无"