"""格式化模块-负责结果格式化、摘要统计和矩阵生成"""


import os
import json
from typing import List, Dict, Any
from ..process_layer.models import SimilarityResult


# ==================== 输出格式函数 ====================
def format_table(results: List[SimilarityResult]) -> str:
    """将结果格式化为表格，基因组ID不显示扩展名"""
    if not results:
        return "没有结果"
    
    # 生成去掉扩展名的显示ID，并计算最大宽度
    display_ids = []
    for r in results:
        id1_disp = os.path.splitext(r.genome1_id)[0]
        id2_disp = os.path.splitext(r.genome2_id)[0]
        display_ids.append((id1_disp, id2_disp))
    
    max_genome1_len = max(len(id1) for id1, _ in display_ids)
    max_genome2_len = max(len(id2) for _, id2 in display_ids)
    genome1_width = max(max_genome1_len, 8)
    genome2_width = max(max_genome2_len, 8)
    
    hashes_width = 8
    shared_width = 8
    jaccard_width = 10
    ani_width = 10

    lines = []
    header = f"{'Genome1':<{genome1_width}} {'Genome2':<{genome2_width}} {'Hashes1':<{hashes_width}} {'Hashes2':<{hashes_width}} {'SharedHashes':<{shared_width}} {'Jaccard':<{jaccard_width}}"
    if results[0].ani is not None:
        header += f" {'ANI':<{ani_width}}"
    lines.append(header)
    lines.append("-" * len(header))

    for r, (id1_disp, id2_disp) in zip(results, display_ids):
        line = f"{id1_disp:<{genome1_width}} {id2_disp:<{genome2_width}} {r.total_hashes1:<{hashes_width}} {r.total_hashes2:<{hashes_width}} {r.shared_hashes:<{shared_width}} {r.jaccard_index:<{jaccard_width}.6f}"
        if r.ani is not None:
            line += f" {r.ani:<{ani_width}.6f}"
        lines.append(line)
    return "\n".join(lines)


def format_csv(results: List[SimilarityResult]) -> str:
    """将结果格式化为CSV，基因组ID不显示扩展名"""
    lines = []
    header = "genome1,genome2,total_hashes1,total_hashes2,shared_hashes,jaccard_index"
    if results[0].ani is not None:
        header += ",ani"
    lines.append(header)

    for r in results:
        id1_disp = os.path.splitext(r.genome1_id)[0]
        id2_disp = os.path.splitext(r.genome2_id)[0]
        row = f"{id1_disp},{id2_disp},{r.total_hashes1},{r.total_hashes2},{r.shared_hashes},{r.jaccard_index:.6f}"
        if r.ani is not None:
            row += f",{r.ani:.6f}"
        lines.append(row)
    return "\n".join(lines)


def format_json(results: List[SimilarityResult]) -> str:
    """将结果格式化为JSON字符串"""
    output = {
        "results": [r.to_dict() for r in results],
        "count": len(results)
    }
    return json.dumps(output, indent=2)




# ==================== 摘要与矩阵生成器类 ====================
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
    



    