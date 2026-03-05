"""文件写入模块"""

import os
import json
import csv
from typing import List, Optional
from ..process_layer.models import SimilarityResult
from .console import ConsoleOutput


class FileWriter:
    """文件写入器类"""
    
    def __init__(self, output_path: str, console: Optional[ConsoleOutput] = None):
        """
        初始化文件写入器
        
        Args:
            output_path: 输出文件路径
            console: 控制台输出对象
        """
        self.output_path = output_path
        self.console = console or ConsoleOutput()
    
    def write_results(self, results: List[SimilarityResult], format: str = 'table'):
        """
        写入结果到文件
        
        Args:
            results: 相似度结果列表
            format: 输出格式
        """
        try:
            # 创建输出目录（如果不存在）
            output_dir = os.path.dirname(self.output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            if format == 'table':
                self._write_table(results)
            elif format == 'csv':
                self._write_csv(results)
            elif format == 'json':
                self._write_json(results)
            
            self.console.print_info(f"结果已写入: {self.output_path}")
            
        except Exception as e:
            self.console.print_error(f"写入文件失败: {e}")
    
    def _write_table(self, results: List[SimilarityResult]):
        """
        写入表格格式
        
        Args:
            results: 相似度结果列表
        """
        with open(self.output_path, 'w') as f:
            # 写入表头
            header = f"{'Genome 1':<20} {'Genome 2':<20} {'Jaccard':<10} {'Shared':<8} {'Total1':<8} {'Total2':<8}"
            if results[0].ani is not None:
                header += f" {'ANI':<10}"
            f.write(header + "\n")
            f.write("-" * len(header) + "\n")
            
            # 写入数据行
            for r in results:
                line = f"{r.genome1_id[:20]:<20} {r.genome2_id[:20]:<20} {r.jaccard_index:<10.6f} {r.shared_hashes:<8} {r.total_hashes1:<8} {r.total_hashes2:<8}"
                if r.ani is not None:
                    line += f" {r.ani:<10.6f}"
                f.write(line + "\n")
    
    def _write_csv(self, results: List[SimilarityResult]):
        """
        写入CSV格式
        
        Args:
            results: 相似度结果列表
        """
        with open(self.output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # 写入表头
            header = ['genome1', 'genome2', 'jaccard_index', 'shared_hashes', 'total_hashes1', 'total_hashes2']
            if results[0].ani is not None:
                header.append('ani')
            writer.writerow(header)
            
            # 写入数据行
            for r in results:
                row = [r.genome1_id, r.genome2_id, f"{r.jaccard_index:.6f}", r.shared_hashes, r.total_hashes1, r.total_hashes2]
                if r.ani is not None:
                    row.append(f"{r.ani:.6f}")
                writer.writerow(row)
    
    def _write_json(self, results: List[SimilarityResult]):
        """
        写入JSON格式
        
        Args:
            results: 相似度结果列表
        """
        output = {
            "results": [r.to_dict() for r in results],
            "count": len(results)
        }
        
        with open(self.output_path, 'w') as f:
            json.dump(output, f, indent=2)