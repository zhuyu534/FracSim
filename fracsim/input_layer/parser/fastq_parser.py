"""FASTQ文件解析器模块"""

import sys
from typing import Generator, Tuple, Union, IO


class FastqParser:
    """FASTQ文件解析器类"""
    
    def parse(self, input_source: Union[str, IO]) -> Generator[Tuple[str, str, str], None, None]:
        """
        解析FASTQ格式数据
        
        Args:
            input_source: 文件路径（str）或已打开的文本文件对象（IO）
            
        Yields:
            Tuple[str, str, str]: (序列ID, 序列, 质量分数)
            
        Raises:
            ValueError: 文件格式错误
        """

        if isinstance(input_source, str):
            f = open(input_source, 'r')
            need_close = True
        else:
            f = input_source
            need_close = False

        line_num = 0
        
        try:
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
                    raise ValueError(
                        f"FASTQ格式错误: 序列长度({len(sequence)})与质量长度({len(quality)})不一致"
                    )

                yield (seq_id, sequence, quality)

        finally:
            if need_close:
                f.close()

    def _validate_sequence(self, seq: str) -> bool:
        valid_chars = set('ATCGUNRYSWKMBDHVatcgunryswkmbdhv')  # 标准碱基 + 模糊码
        return all(c in valid_chars for c in seq)

    def _find_invalid_chars(self, seq: str) -> str:
        valid_chars = set('ATCGUNRYSWKMBDHVatcgunryswkmbdhv')
        invalid_positions = []
        invalid_chars_found = set()
        for i, c in enumerate(seq, 1):
            if c not in valid_chars:
                invalid_positions.append(str(i))
                invalid_chars_found.add(c)
        if invalid_positions:
            return f"位置: {', '.join(invalid_positions)}，非法字符: {', '.join(invalid_chars_found)}"
        return "无"