"""控制台输出模块"""

import sys
from typing import List, Dict, Any
from ..process_layer.models import SimilarityResult


class ConsoleOutput:
    """控制台输出类"""
    
    def __init__(self, verbose: bool = False):
        """
        初始化控制台输出
        
        Args:
            verbose: 是否输出详细信息
        """
        self.verbose = verbose
    
    def print_info(self, message: str):
        """
        打印信息
        
        Args:
            message: 信息内容
        """
        if self.verbose:
            sys.stderr.write(f"[INFO] {message}\n")
    
    def print_warning(self, message: str):
        """
        打印警告
        
        Args:
            message: 警告内容
        """
        sys.stderr.write(f"[WARNING] {message}\n")
    
    def print_error(self, message: str):
        """
        打印错误
        
        Args:
            message: 错误内容
        """
        sys.stderr.write(f"[ERROR] {message}\n")
    
    def print_results(self, results: List[SimilarityResult], format: str = 'table'):
        """
        打印结果
        
        Args:
            results: 相似度结果列表
            format: 输出格式
        """
        if not results:
            print("没有结果")
            return
        
        if format == 'table':
            self._print_table(results)
        elif format == 'csv':
            self._print_csv(results)
        elif format == 'json':
            self._print_json(results)
    
    def _print_table(self, results: List[SimilarityResult]):
        """
        打印表格格式
        
        Args:
            results: 相似度结果列表
        """
        # 打印表头
        header = f"{'Genome 1':<20} {'Genome 2':<20} {'Jaccard':<10} {'SharedHashes':<8} {'Hashes1':<8} {'Hashes2':<8}"
        if results[0].ani is not None:
            header += f" {'ANI':<10}"
        print(header)
        print("-" * len(header))
        
        # 打印数据行
        for r in results:
            line = f"{r.genome1_id[:20]:<20} {r.genome2_id[:20]:<20} {r.jaccard_index:<10.6f} {r.shared_hashes:<8} {r.total_hashes1:<8} {r.total_hashes2:<8}"
            if r.ani is not None:
                line += f" {r.ani:<10.6f}"
            print(line)
    
    def _print_csv(self, results: List[SimilarityResult]):
        """
        打印CSV格式
        
        Args:
            results: 相似度结果列表
        """
        # 打印表头
        header = "genome1,genome2,jaccard_index,shared_hashes,total_hashes1,total_hashes2"
        if results[0].ani is not None:
            header += ",ani"
        print(header)
        
        # 打印数据行
        for r in results:
            line = f"{r.genome1_id},{r.genome2_id},{r.jaccard_index:.6f},{r.shared_hashes},{r.total_hashes1},{r.total_hashes2}"
            if r.ani is not None:
                line += f",{r.ani:.6f}"
            print(line)
    
    def _print_json(self, results: List[SimilarityResult]):
        """
        打印JSON格式
        
        Args:
            results: 相似度结果列表
        """
        import json
        
        output = {
            "results": [r.to_dict() for r in results],
            "count": len(results)
        }
        
        print(json.dumps(output, indent=2))
    
    def print_progress(self, current: int, total: int, message: str = ""):
        """
        打印进度
        
        Args:
            current: 当前进度
            total: 总数
            message: 额外信息
        """
        if not self.verbose:
            return
        
        percentage = (current / total) * 100
        bar_length = 50
        filled_length = int(bar_length * current // total)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stderr.write(f"\r[{bar}] {percentage:.1f}% ({current}/{total}) {message}")
        if current == total:
            sys.stderr.write("\n")