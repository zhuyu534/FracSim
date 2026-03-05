"""验证工具模块"""

import os
from typing import List, Union


class Validator:
    """验证器类"""
    
    @staticmethod
    def validate_kmer_size(k: int) -> bool:
        """
        验证k-mer长度
        
        Args:
            k: k-mer长度
            
        Returns:
            bool: 是否有效
        """
        return 1 <= k <= 64
    
    @staticmethod
    def validate_scaled(scaled: float) -> bool:
        """
        验证采样率
        
        Args:
            scaled: 采样率
            
        Returns:
            bool: 是否有效
        """
        return 0 < scaled <= 1
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """
        验证文件路径
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否有效
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def validate_sequence(seq: str) -> bool:
        """
        验证序列
        
        Args:
            seq: 序列字符串
            
        Returns:
            bool: 是否有效
        """
        if not seq:
            return False
        
        valid_chars = set('ATCGNatcgn')
        return all(c in valid_chars for c in seq)