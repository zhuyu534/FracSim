"""k-mer计算模块"""

import sys
from typing import Set, Dict, Generator, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils.hash import HashFunction


class KmerGenerator:
    """k-mer生成器类"""
    
    def __init__(self, k: int, seed: int = 42, threads: int = 1):
        """
        初始化k-mer生成器
        
        Args:
            k: k-mer长度
            seed: 哈希种子
            threads: 线程数
        """
        self.k = k
        self.threads = threads
        self.hash_func = HashFunction(seed)
    
    def generate_kmers(self, sequence: str, canonical: bool = True) -> Generator[str, None, None]:
        """
        从序列生成k-mer
        
        Args:
            sequence: 序列字符串
            canonical: 是否使用正则形式（取正反链中较小的）
            
        Yields:
            str: k-mer字符串
        """
        seq_upper = sequence.upper()
        seq_len = len(seq_upper)
        
        for i in range(seq_len - self.k + 1):
            kmer = seq_upper[i:i + self.k]
            
            if 'N' in kmer:  # 跳过包含N的k-mer
                continue
            
            if canonical:
                # 计算正则形式（取正反链中字典序较小的）
                rev_comp = self._reverse_complement(kmer)
                kmer = min(kmer, rev_comp)
            
            yield kmer
    
    def get_kmer_set(self, sequence: str, canonical: bool = True) -> Set[str]:
        """
        获取序列的所有k-mer集合
        
        Args:
            sequence: 序列字符串
            canonical: 是否使用正则形式
            
        Returns:
            Set[str]: k-mer集合
        """
        kmers = set()
        for kmer in self.generate_kmers(sequence, canonical):
            kmers.add(kmer)
        return kmers
    
    def get_kmer_frequencies(self, sequence: str, canonical: bool = True) -> Dict[str, int]:
        """
        获取k-mer频率
        
        Args:
            sequence: 序列字符串
            canonical: 是否使用正则形式
            
        Returns:
            Dict[str, int]: k-mer频率字典
        """
        freq = {}
        for kmer in self.generate_kmers(sequence, canonical):
            freq[kmer] = freq.get(kmer, 0) + 1
        return freq
    
    def get_kmer_hashes(self, sequence: str, canonical: bool = True) -> Set[int]:
        """
        获取序列所有k-mer的哈希值
        
        Args:
            sequence: 序列字符串
            canonical: 是否使用正则形式
            
        Returns:
            Set[int]: 哈希值集合
        """
        hashes = set()
        
        if self.threads > 1 and len(sequence) > 100000:
            # 并行处理长序列
            hashes = self._parallel_kmer_hash(sequence, canonical)
        else:
            # 串行处理
            for kmer in self.generate_kmers(sequence, canonical):
                hash_val = self.hash_func.get_hash(kmer)
                hashes.add(hash_val)
        
        return hashes
    
    def _parallel_kmer_hash(self, sequence: str, canonical: bool) -> Set[int]:
        """
        并行计算k-mer哈希
        
        Args:
            sequence: 序列字符串
            canonical: 是否使用正则形式
            
        Returns:
            Set[int]: 哈希值集合
        """
        hashes = set()
        seq_len = len(sequence)
        chunk_size = seq_len // self.threads
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for i in range(self.threads):
                start = i * chunk_size
                end = start + chunk_size + self.k if i < self.threads - 1 else seq_len
                
                if start < seq_len - self.k + 1:
                    future = executor.submit(
                        self._process_chunk,
                        sequence[start:end],
                        start,
                        canonical
                    )
                    futures.append(future)
            
            for future in as_completed(futures):
                hashes.update(future.result())
        
        return hashes
    
    def _process_chunk(self, chunk: str, offset: int, canonical: bool) -> Set[int]:
        """
        处理序列片段
        
        Args:
            chunk: 序列片段
            offset: 起始位置偏移
            canonical: 是否使用正则形式
            
        Returns:
            Set[int]: 哈希值集合
        """
        hashes = set()
        
        for i in range(len(chunk) - self.k + 1):
            kmer = chunk[i:i + self.k].upper()
            
            if 'N' in kmer:
                continue
            
            if canonical:
                rev_comp = self._reverse_complement(kmer)
                kmer = min(kmer, rev_comp)
            
            hash_val = self.hash_func.get_hash(kmer)
            hashes.add(hash_val)
        
        return hashes
    
    def _reverse_complement(self, seq: str) -> str:
        """
        计算序列的反向互补
        
        Args:
            seq: 序列字符串
            
        Returns:
            str: 反向互补序列
        """
        complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        return ''.join(complement.get(base, base) for base in reversed(seq))