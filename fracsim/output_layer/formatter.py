"""格式化模块-负责结果格式化、摘要统计和矩阵生成"""


import os
import json
from typing import List, Dict, Any
from ..process_layer.models import SimilarityResult


# ==================== 输出格式函数 ====================

def strip_extensions(filename: str) -> str:
    """
    去除文件名中的常见序列格式扩展名和压缩扩展名，
    例如 'GCA_123.fna.gz' -> 'GCA_123'
    """
    # 常见序列扩展名
    seq_exts = {'.fasta', '.fa', '.fna', '.ffn', '.frn', '.fastq', '.fq'}
    # 压缩扩展名
    compress_exts = {'.gz', '.bz2', '.xz', '.zip'}
    
    base = filename
    # 反复去除已知后缀，直到没有变化
    while True:
        name, ext = os.path.splitext(base)
        if ext in compress_exts or ext in seq_exts:
            base = name
        else:
            break
    return base

def format_table(results: List[SimilarityResult]) -> str:
    # 计算显示用的纯名称列表
    display_ids = [(strip_extensions(r.genome1_id), strip_extensions(r.genome2_id)) for r in results]
    # 根据这些显示名称计算列宽
    max_len1 = max(len(id1) for id1, _ in display_ids)
    max_len2 = max(len(id2) for _, id2 in display_ids)
    # 设置最小宽度
    w1 = max(max_len1, 8)
    w2 = max(max_len2, 8)
    
    lines = []
    header = f"{'Genome1':<{w1}} {'Genome2':<{w2}} {'Hashes1':<8} {'Hashes2':<8} {'SharedHashes':<8} {'Jaccard':<10}"
    if results[0].ani is not None:
        header += f" {'ANI':<10}"
    lines.append(header)
    lines.append("-" * len(header))
    
    for r, (id1_disp, id2_disp) in zip(results, display_ids):
        line = f"{id1_disp:<{w1}} {id2_disp:<{w2}} {r.total_hashes1:<8} {r.total_hashes2:<8} {r.shared_hashes:<8} {r.jaccard_index:<10.6f}"
        if r.ani is not None:
            line += f" {r.ani:<10.4f}"
        lines.append(line)
    return "\n".join(lines)


def format_csv(results: List[SimilarityResult]) -> str:
    lines = []
    header = "genome1,genome2,total_hashes1,total_hashes2,shared_hashes,jaccard_index"
    if results[0].ani is not None:
        header += ",ani"
    lines.append(header)
    for r in results:
        id1_disp = strip_extensions(r.genome1_id)
        id2_disp = strip_extensions(r.genome2_id)
        row = f"{id1_disp},{id2_disp},{r.total_hashes1},{r.total_hashes2},{r.shared_hashes},{r.jaccard_index:.6f}"
        if r.ani is not None:
            row += f",{r.ani:.4f}"
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
    



    