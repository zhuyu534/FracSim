"""ANI计算模块"""

import math
from typing import Optional
from .models import SimilarityResult


class ANICalculator:
    """ANI计算器类"""
    
    def __init__(self, genome_size_correction: bool = True):
        """
        初始化ANI计算器
        
        Args:
            genome_size_correction: 是否进行基因组大小校正
        """
        self.genome_size_correction = genome_size_correction
    
    def calculate_ani_from_jaccard(self, similarity: SimilarityResult, k: int) -> Optional[float]:
        """
        从Jaccard指数估算ANI,返回百分比值（0-100）
        
        基于Mash论文中的公式：
        ANI ≈ 1 - (1/k) * ln(2J/(1+J))
        
        Args:
            similarity: 相似度结果
            k: k-mer长度
            
        Returns:
            Optional[float]: ANI值
        """
        jaccard = similarity.jaccard_index
        
        # 检查Jaccard指数是否有效
        if jaccard <= 0:
            return 0.0
        
        if jaccard >= 1:
            return 100.0
        
        try:
            # 计算Mash距离
            mash_dist = -(1.0 / k) * math.log(2 * jaccard / (1 + jaccard))
            
            # 转换为ANI
            ani = 1.0 - mash_dist
            
            # 应用基因组大小校正
            if self.genome_size_correction:
                ani = self._apply_size_correction(ani, similarity)
            
            # 限制在[0,1]范围内
            ani = max(0.0, min(1.0, ani))
            ani = ani * 100.0  # 转换为百分比
            return ani
            
        except (ValueError, ZeroDivisionError):
            return None
    
    
    def _apply_size_correction(self, ani: float, similarity: SimilarityResult) -> float:
        """
        应用基因组大小校正
        
        Args:
            ani: 原始ANI值
            similarity: 相似度结果
            
        Returns:
            float: 校正后的ANI值
        """
        # 如果两个基因组大小差异过大，进行校正
        size_ratio = similarity.total_kmers1 / similarity.total_kmers2
        size_ratio = min(size_ratio, 1.0 / size_ratio)  # 确保 ≤ 1
        
        if size_ratio < 0.5:  # 大小差异超过2倍
            # 应用简单的线性校正
            correction_factor = 1.0 + (1.0 - size_ratio) * 0.1
            ani = ani * correction_factor
        
        return ani