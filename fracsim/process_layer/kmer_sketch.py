"""k-mer计算，FracMinHash素描生成模块"""


from typing import Set
from .models import SketchData, GenomeData
from ..utils.hash import HashFunction
from typing import Set,  Generator
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

        if self.threads > 1 and len(sequence) > 100000:  # 避免小序列的并行开销
            # 并行处理长序列
            hashes = self._parallel_kmer_hash(sequence, canonical)
        else:
            # 串行处理
            for kmer in self.generate_kmers(sequence, canonical):
                hash_val = self.hash_func.get_hash(kmer)
                if hash_val < max_hash:  # 筛选
                    hashes.add(hash_val)
        
        return hashes
    
    def _parallel_kmer_hash(self, sequence: str,  canonical: bool) -> Set[int]:
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
    
    def _process_chunk(self, chunk: str, max_hash: int, offset: int, canonical: bool) -> Set[int]:
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
        AMBIGUOUS_BASES = set('RYSWKMBDHVryswkmbdhv')

        for i in range(len(chunk) - self.k + 1):
            kmer = chunk[i:i + self.k].upper()
            
            if 'N' in kmer or any(c in AMBIGUOUS_BASES for c in kmer):
                continue
            
            if canonical:
                rev_comp = self._reverse_complement(kmer)
                kmer = min(kmer, rev_comp)
            
            hash_val = self.hash_func.get_hash(kmer)
            if hash_val < max_hash:
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
    

# ---------------------------------------------------
#----------------------------------------------------
#----------------------------------------------------

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
        max_hash = self._calculate_max_hash()
        all_hashes = set()
        total_kmers = 0

        # 遍历所有序列，合并哈希集合
        for sequence in genome_data.sequences:
            # 获取当前序列的过滤后哈希集合
            seq_hashes = self.kmer_gen.get_kmer_hashes(sequence, max_hash)
            all_hashes.update(seq_hashes)  # 合并哈希集合
            sketch_size = len(all_hashes)
            
            # 累加总窗口数
            total_kmers += len(sequence) - self.k + 1

        
        # 创建素描数据
        sketch = SketchData(
            genome_id=genome_data.seq_id,
            kmer_size=self.k,
            scaled=self.scaled,
            seed=self.seed,
            hashes=all_hashes,
            total_kmers=total_kmers,
            sketch_size=sketch_size

        )
        
        return sketch
    
    
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

