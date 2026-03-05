"""格式化模块"""

from typing import List, Dict, Any
from ..process_layer.models import SimilarityResult


class OutputFormatter:
    """输出格式化器类"""
    
    @staticmethod
    def format_summary(results: List[SimilarityResult]) -> Dict[str, Any]:
        """
        格式化摘要信息
        
        Args:
            results: 相似度结果列表
            
        Returns:
            Dict: 摘要信息
        """
        if not results:
            return {"count": 0}
        
        jaccard_values = [r.jaccard_index for r in results]
        ani_values = [r.ani for r in results if r.ani is not None]
        
        summary = {
            "count": len(results),
            "jaccard": {
                "min": min(jaccard_values),
                "max": max(jaccard_values),
                "mean": sum(jaccard_values) / len(jaccard_values),
                "median": sorted(jaccard_values)[len(jaccard_values) // 2]
            }
        }
        
        if ani_values:
            summary["ani"] = {
                "min": min(ani_values),
                "max": max(ani_values),
                "mean": sum(ani_values) / len(ani_values),
                "median": sorted(ani_values)[len(ani_values) // 2]
            }
        
        return summary
    
    @staticmethod
    def format_matrix(results: List[SimilarityResult], genome_ids: List[str]) -> List[List[float]]:
        """
        格式化相似度矩阵
        
        Args:
            results: 相似度结果列表
            genome_ids: 基因组ID列表
            
        Returns:
            List[List[float]]: 相似度矩阵
        """
        n = len(genome_ids)
        id_to_idx = {id: i for i, id in enumerate(genome_ids)}
        
        # 初始化矩阵
        matrix = [[0.0] * n for _ in range(n)]
        
        # 填充矩阵
        for r in results:
            i = id_to_idx[r.genome1_id]
            j = id_to_idx[r.genome2_id]
            matrix[i][j] = r.jaccard_index
            matrix[j][i] = r.jaccard_index
        
        # 对角线设为1
        for i in range(n):
            matrix[i][i] = 1.0
        
        return matrix