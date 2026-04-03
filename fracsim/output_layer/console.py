"""控制台输出模块"""

import sys
from typing import List
from ..process_layer.models import SimilarityResult
from .formatter import format_table, format_csv, format_json, format_tsv


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
            print(format_table(results))
        elif format == 'csv':
            print(format_csv(results))
        elif format == 'json':
            print(format_json(results))
        elif format == 'tsv':
            print(format_tsv(results))
        else:
            self.print_warning(f"未知格式: {format}，使用默认表格格式")
            print(format_table(results))

    
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