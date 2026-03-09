"""文件写入模块"""

import os
from typing import List, Optional
from ..process_layer.models import SimilarityResult
from .console import ConsoleOutput
from .formatter import format_table, format_csv, format_json


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

        if format == 'table':
            ext = os.path.splitext(self.output_path)[1].lower()
            if ext == '.json':
                format = 'json'
            elif ext == '.csv':
                format = 'csv'

        try:
            # 创建输出目录（如果不存在）
            output_dir = os.path.dirname(self.output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 根据格式获取内容
            if format == 'table':
                content = format_table(results)
            elif format == 'csv':
                content = format_csv(results)
            elif format == 'json':
                content = format_json(results)
            else:
                self.console.print_warning(f"未知格式: {format}，使用默认表格格式")
                content = format_table(results)

            # 写入文件
            with open(self.output_path, 'w') as f:
                f.write(content)

            self.console.print_info(f"结果已写入: {self.output_path}")

        except Exception as e:
            self.console.print_error(f"写入文件失败: {e}")
    
    