"""内部数据模型模块"""

from dataclasses import dataclass, field
from typing import Dict, Set, Optional, List
from datetime import datetime


@dataclass
class GenomeData:
    """基因组数据类"""
    file_path: str
    seq_id: str
    sequences: List[str]
    quality: Optional[List[str]] = None
    length: int = 0
    gc_content: float = 0.0
    
    
    def __post_init__(self):
        total_len = 0
        total_gc = 0
        for seq in self.sequences:        
            seq_upper = seq.upper()
            total_len += len(seq_upper)
            total_gc += seq_upper.count('G') + seq_upper.count('C')
        self.length = total_len
        if total_len > 0:
            self.gc_content = total_gc / total_len * 100


@dataclass
class SketchData:
    """素描数据类"""
    genome_id: str
    kmer_size: int
    scaled: int
    seed: int
    hashes: Set[int] = field(default_factory=set)
    total_kmers: int = 0
    sketch_size: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        self.sketch_size = len(self.hashes)


@dataclass
class SimilarityResult:
    """相似度结果类"""
    genome1_id: str
    genome2_id: str
    jaccard_index: float
    ani: Optional[float] = None
    shared_hashes: int = 0
    total_hashes1: int = 0
    total_hashes2: int = 0
    total_kmers1: int = 0
    total_kmers2: int = 0
    
    def to_dict(self) -> Dict:
        """转换为字典"""

        # def strip_extensions(filename: str) -> str:
        #     base = filename
            
        #     # 去除压缩扩展名
        #     compress_exts = ['.gz', '.bz2', '.xz', '.zip']
        #     for ext in compress_exts:
        #         if base.endswith(ext):
        #             base = base[:-len(ext)]
        #             break

        #     # 去除序列扩展名
        #     seq_exts = ['.fasta', '.fa', '.fna', '.ffn', '.frn', '.fastq', '.fq']
        #     for ext in seq_exts:
        #         if base.endswith(ext):
        #             base = base[:-len(ext)]
        #             break
        #     return base

        result = {
            'genome1': self.genome1_id,
            'genome2': self.genome2_id,
            'total_hashes1': self.total_hashes1,
            'total_hashes2': self.total_hashes2,
            'shared_hashes': self.shared_hashes,
            'jaccard_index': round(self.jaccard_index, 6),  # 保留6位小数
        }
        if self.ani is not None:
            result['ani'] = round(self.ani, 4)  # 保留4位小数
        return result