"""FracMinHash素描生成模块"""

import sys
from typing import Set, Optional
from .models import SketchData, GenomeData
from .kmer import KmerGenerator
from ..utils.hash import HashFunction


class FracMinHashSketch:
    """FracMinHash素描生成器类"""
    
    def __init__(self, k: int, scaled: float, seed: int = 42, threads: int = 1):
        """
        初始化FracMinHash素描生成器
        
        Args:
            k: k-mer长度
            scaled: 采样率
            seed: 哈希种子
            threads: 线程数
        """
        self.k = k
        self.scaled = scaled
        self.seed = seed
        self.threads = threads
        self.kmer_gen = KmerGenerator(k, seed, threads)
        self.hash_func = HashFunction(seed)
    
    def create_sketch(self, genome_data: GenomeData) -> SketchData:
        """
        创建基因组素描
        
        Args:
            genome_data: 基因组数据
            
        Returns:
            SketchData: 素描数据
        """
        # 计算最大哈希阈值
        max_hash = self._calculate_max_hash()
        
        # 获取所有k-mer哈希并筛选
        all_hashes = self.kmer_gen.get_kmer_hashes(genome_data.sequence)
        total_kmers = len(all_hashes)
        
        # 筛选哈希值小于阈值的k-mer
        selected_hashes = {h for h in all_hashes if h < max_hash}
        
        # 创建素描数据
        sketch = SketchData(
            genome_id=genome_data.seq_id,
            kmer_size=self.k,
            scaled=self.scaled,
            seed=self.seed,
            hashes=selected_hashes,
            total_kmers=total_kmers
        )
        
        return sketch
    
    def create_sketch_from_hashes(self, genome_id: str, hashes: Set[int]) -> SketchData:
        """
        从已有哈希集合创建素描
        
        Args:
            genome_id: 基因组ID
            hashes: 哈希集合
            
        Returns:
            SketchData: 素描数据
        """
        max_hash = self._calculate_max_hash()
        selected_hashes = {h for h in hashes if h < max_hash}
        
        return SketchData(
            genome_id=genome_id,
            kmer_size=self.k,
            scaled=self.scaled,
            seed=self.seed,
            hashes=selected_hashes,
            total_kmers=len(hashes)
        )
    
    def _calculate_max_hash(self) -> int:
        """
        计算最大哈希阈值
        
        FracMinHash原理：保留哈希值小于 max_hash 的k-mer
        max_hash = floor(2^64 * scaled)
        
        Returns:
            int: 最大哈希阈值
        """
        # 使用64位哈希空间
        max_64bit = 2**64 - 1
        return int(max_64bit * self.scaled)
    
    def merge_sketches(self, sketches: list) -> SketchData:
        """
        合并多个素描
        
        Args:
            sketches: 素描列表
            
        Returns:
            SketchData: 合并后的素描
        """
        if not sketches:
            raise ValueError("素描列表为空")
        
        merged_hashes = set()
        total_kmers = 0
        
        for sketch in sketches:
            merged_hashes.update(sketch.hashes)
            total_kmers += sketch.total_kmers
        
        return SketchData(
            genome_id=f"merged_{len(sketches)}_genomes",
            kmer_size=self.k,
            scaled=self.scaled,
            seed=self.seed,
            hashes=merged_hashes,
            total_kmers=total_kmers
        )