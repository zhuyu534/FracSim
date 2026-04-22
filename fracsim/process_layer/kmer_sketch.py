"""k-mer计算，FracMinHash素描生成模块"""


import sys
from .models import SketchData, GenomeData
from ..utils.hash import HashFunction
from typing import Set,  Generator
from concurrent.futures import ProcessPoolExecutor, as_completed


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
        self.hash_func = HashFunction(seed)
    
    def generate_kmers(self, sequence: str, canonical: bool = True) -> Generator[str, None, None]:
        """
        从序列生成k-mer
        
        Args:
            sequence: 基因组序列
            canonical: 是否使用正则形式（取正反链中较小的）
            
        Yields:
            str: k-mer字符串
        """
        seq_upper = sequence.upper()
        seq_len = len(seq_upper)
        
        for i in range(seq_len - self.k + 1):  # 滑动窗口法提取k-mer
            kmer = seq_upper[i:i + self.k]
            
            if canonical:
                # 计算正则形式
                rev_comp = self._reverse_complement(kmer)  # # 计算反向互补序列
                kmer = min(kmer, rev_comp)  # 取正反链中字典序较小的
            
            # 过滤包含 N 的 k‑mer（最常见模糊碱基）
            if 'N' in kmer:
                continue

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
        return kmers  # 得到k-mer集合
    
    
    def get_kmer_hashes(self, sequence: str, max_hash: int, canonical: bool = True) -> Set[int]:
        """
        获取所有k-mer的哈希值
        
        Args:
            sequence: 序列字符串
            max_hash: 最大哈希阈值（由调用者提供）
            canonical: 是否使用正则形式
            
        Returns:
            Set[int]: 哈希值集合
        """
        hashes = set()

        
        # 串行处理
        for kmer in self.generate_kmers(sequence, canonical):
            hash_val = self.hash_func.get_hash(kmer)
            if hash_val < max_hash:  # 筛选
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
    

 # 辅助函数：供多进程调用，计算单条序列的哈希集合
def _process_sequence_for_sketch(sequence: str, k: int, max_hash: int, seed: int, canonical: bool) -> Set[int]:
    """
    子进程任务：计算单条序列的FracMinHash哈希集合
    
    Args:
        sequence: 序列字符串
        k: k-mer长度
        max_hash: 最大哈希阈值
        seed: 哈希种子
        canonical: 是否使用正则形式
        
    Returns:
        Set[int]: 哈希值集合
    """
    # 每个子进程独立创建KmerGenerator，避免传递不可序列化对象
    kg = KmerGenerator(k, seed, threads=1)
    return kg.get_kmer_hashes(sequence, max_hash, canonical)
   


# ---------------------------------------------------
#----------------------------------------------------
#----------------------------------------------------

class FracMinHashSketch:
    """FracMinHash素描生成器类（支持多进程并行）"""
    
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
        max_hash = self._calculate_max_hash()
        sequences = genome_data.sequences

        # 计算总k-mer数（串行，仅用长度）
        total_kmers = 0
        for seq in sequences:
            if len(seq) >= self.k:
                total_kmers += len(seq) - self.k + 1
        
        # 判断是否启用多进程
        if self.threads > 1 and len(sequences) > 1:
            all_hashes = self._parallel_process(sequences, max_hash)
        else:
            all_hashes = self._serial_process(sequences, max_hash)
            
 
        # 创建素描数据
        sketch = SketchData(
            genome_id=genome_data.seq_id,
            kmer_size=self.k,
            scaled=self.scaled,
            seed=self.seed,
            hashes=all_hashes,
            total_kmers=total_kmers,
            sketch_size=len(all_hashes)

        )
        
        return sketch
    

    def _serial_process(self, sequences: list, max_hash: int) -> Set[int]:
        """串行处理所有序列"""
        all_hashes = set()
        for seq in sequences:
            seq_hashes = self.kmer_gen.get_kmer_hashes(seq, max_hash, canonical=True)
            all_hashes.update(seq_hashes)
        return all_hashes
    
    def _parallel_process(self, sequences: list, max_hash: int) -> Set[int]:
        """使用进程池并行处理所有序列"""
        all_hashes = set()
        with ProcessPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for seq in sequences:
                # 跳过长度小于k的序列（不会产生k-mer）
                if len(seq) < self.k:
                    continue
                future = executor.submit(
                    _process_sequence_for_sketch,
                    seq, self.k, max_hash, self.seed, True
                )
                futures.append(future)
            
            for future in as_completed(futures):
                try:
                    seq_hashes = future.result()
                    all_hashes.update(seq_hashes)
                except Exception as e:
                    # 实际项目中可改用日志模块
                    print(f"Error in subprocess: {e}", file=sys.stderr)
        return all_hashes


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

