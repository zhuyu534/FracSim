"""Jaccard计算模块"""


from .models import SketchData, SimilarityResult


class JaccardCalculator:
    """Jaccard指数计算器类"""
    
    @staticmethod
    def calculate_jaccard(sketch1: SketchData, sketch2: SketchData) -> SimilarityResult:
        """
        计算两个素描之间的Jaccard指数
        
        J(A,B) = |A∩B| / |A∪B|
        
        Args:
            sketch1: 素描1
            sketch2: 素描2
            
        Returns:
            SimilarityResult: 相似度结果
        """
        # 计算交集
        intersection = sketch1.hashes.intersection(sketch2.hashes)
        intersection_size = len(intersection)
        
        # 计算并集
        union_size = len(sketch1.hashes) + len(sketch2.hashes) - intersection_size
        
        # 计算Jaccard指数
        if union_size > 0:
            jaccard = intersection_size / union_size
        else:
            jaccard = 0.0
        
        # 创建结果
        result = SimilarityResult(
            genome1_id=sketch1.genome_id,
            genome2_id=sketch2.genome_id,
            jaccard_index=jaccard,
            shared_hashes=intersection_size,
            total_hashes1=sketch1.sketch_size,
            total_hashes2=sketch2.sketch_size,
            total_kmers1=sketch1.total_kmers,
            total_kmers2=sketch2.total_kmers
        )
        
        return result
    