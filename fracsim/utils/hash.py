"""哈希函数模块"""

import hashlib
import mmh3
from typing import Union


class HashFunction:
    """哈希函数类"""
    
    def __init__(self, seed: int = 42):
        """
        初始化哈希函数
        
        Args:
            seed: 随机种子
        """
        self.seed = seed
    
    def murmur_hash3(self, kmer: str) -> int:
        """
        使用MurmurHash3计算k-mer的哈希值
        
        Args:
            kmer: k-mer字符串
            
        Returns:
            int: 哈希值
        """
        return mmh3.hash64(kmer, self.seed)[0]
    
    def md5_hash(self, kmer: str) -> int:
        """
        使用MD5计算k-mer的哈希值（备用）
        
        Args:
            kmer: k-mer字符串
            
        Returns:
            int: 哈希值
        """
        return int(hashlib.md5(kmer.encode()).hexdigest()[:16], 16)
    
    def get_hash(self, kmer: str, method: str = 'murmur') -> int:
        """
        获取k-mer的哈希值
        
        Args:
            kmer: k-mer字符串
            method: 哈希方法 ('murmur' 或 'md5')
            
        Returns:
            int: 哈希值
        """
        if method == 'murmur':
            return self.murmur_hash3(kmer)
        else:
            return self.md5_hash(kmer)