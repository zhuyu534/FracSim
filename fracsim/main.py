"""主程序入口"""

import time
import sys
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .version import __version__
from .input_layer import parse_arguments, FileReader
from .process_layer import (
    KmerGenerator, FracMinHashSketch, 
    JaccardCalculator, ANICalculator,
    GenomeData, SketchData, SimilarityResult
)
from .output_layer import ConsoleOutput, FileWriter, OutputFormatter


class GenomeSimilarity:
    """基因组相似度计算主类"""
    
    def __init__(self, args):
        """
        初始化
        
        Args:
            args: 命令行参数
        """
        self.args = args
        self.console = ConsoleOutput(verbose=args.verbose)
        self.file_reader = FileReader(verbose=args.verbose)
        
        # 初始化处理组件
        self.kmer_gen = KmerGenerator(args.kmer_size, args.seed, args.threads)
        self.sketch_gen = FracMinHashSketch(
            args.kmer_size, args.scaled, args.seed, args.threads
        )
        self.jaccard_calc = JaccardCalculator()
        self.ani_calc = ANICalculator(genome_size_correction=True)
        
        # 存储数据
        self.genome_data: Dict[str, GenomeData] = {}
        self.sketches: Dict[str, SketchData] = {}
        self.results: List[SimilarityResult] = []
    
    def run(self):
        """运行主流程"""
        self.console.print_info(f"FracSim v{__version__}")

        # 始终初始化计时器
        timers = {}
        start_total = time.perf_counter()
        
        # 1. 获取文件列表
        file_list = self.file_reader.get_file_list(
            self.args.input, self.args.list
        )
        self.console.print_info(f"处理 {len(file_list)} 个文件")
        
        # 2. 读取基因组数据
        t0 = time.perf_counter()
        self._load_genomes(file_list)
        timers['读取文件'] = time.perf_counter() - t0
        
        # 3. 生成素描
        t0 = time.perf_counter()
        self._generate_sketches()
        timers['生成素描'] = time.perf_counter() - t0
        
        # 4. 计算相似度
        t0 = time.perf_counter()
        self._calculate_similarities()
        timers['计算相似度'] = time.perf_counter() - t0
        
        # 5. 输出结果
        t0 = time.perf_counter()
        self._output_results()
        timers['输出结果'] = time.perf_counter() - t0

        timers['总耗时'] = time.perf_counter() - start_total

        # 仅在 verbose 模式下输出性能统计
        if self.args.verbose:
            self.console.print_info("\n性能统计:")
            for name, t in timers.items():
                self.console.print_info(f"  {name}: {t:.3f} 秒")
    
    def _load_genomes(self, file_list: List[str]):
        """
        加载基因组数据（每个文件作为一个整体）
        
        Args:
            file_list: 文件列表
        """
        self.console.print_info("读取基因组数据...")
        
        for file_path in file_list:
            try:
                # 使用 read_genome 读取整个文件
                genome = self.file_reader.read_genome(file_path)
                self.genome_data[genome.seq_id] = genome
                
                self.console.print_info(
                    f"加载: {genome.seq_id} | 序列数: {len(genome.sequences)} | "
                    f"总长度: {genome.length} bp | GC: {genome.gc_content:.2f}%"
                )
            except Exception as e:
                self.console.print_error(f"加载失败 {file_path}: {e}")
        
        self.console.print_info(f"成功加载 {len(self.genome_data)} 个基因组")
    
    def _generate_sketches(self):
        """生成素描"""
        self.console.print_info("生成FracMinHash素描...")
        
        total = len(self.genome_data)
        for i, (seq_id, genome) in enumerate(self.genome_data.items(), 1):           
            try:
                sketch = self.sketch_gen.create_sketch(genome)
                self.sketches[seq_id] = sketch
                
                if self.args.verbose:
                    sys.stderr.write("\n") 
                self.console.print_info(
                    f"素描: {seq_id} | k={sketch.kmer_size} | "
                    f"总k-mer: {sketch.total_kmers} | 采样: {sketch.sketch_size}"
                )
                self.console.print_progress(i, total, f"处理 {seq_id}")
            except Exception as e:
                self.console.print_error(f"生成素描失败 {seq_id}: {e}")
    
    def _calculate_similarities(self):
        """计算相似度"""
        self.console.print_info("计算基因组相似度...")
        
        genome_ids = list(self.sketches.keys())
        n = len(genome_ids)
        
        if n < 2:
            self.console.print_warning("至少需要2个基因组才能计算相似度")
            return
        
        total_pairs = n * (n - 1) // 2
        current = 0
        
        # 使用线程池并行计算
        with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
            futures = []
            
            for i in range(n):
                for j in range(i + 1, n):
                    future = executor.submit(
                        self._compute_pair,
                        genome_ids[i],
                        genome_ids[j]
                    )
                    futures.append(future)
            
            for future in as_completed(futures):
                current += 1
                self.console.print_progress(current, total_pairs, "计算相似度")
                
                try:
                    result = future.result()
                    if result.jaccard_index >= self.args.min_similarity:
                        self.results.append(result)
                except Exception as e:
                    self.console.print_error(f"计算失败: {e}")
        
        self.console.print_info(f"完成 {len(self.results)} 对相似度计算")
    
    def _compute_pair(self, id1: str, id2: str) -> SimilarityResult:
        """
        计算一对基因组的相似度
        
        Args:
            id1: 基因组1 ID
            id2: 基因组2 ID
            
        Returns:
            SimilarityResult: 相似度结果
        """
        sketch1 = self.sketches[id1]
        sketch2 = self.sketches[id2]
        
        # 计算Jaccard指数
        result = self.jaccard_calc.calculate_jaccard(sketch1, sketch2)
        
        # 计算ANI（如果需要）
        if self.args.ani:
            ani = self.ani_calc.calculate_ani_from_jaccard(result, self.args.kmer_size)
            result.ani = ani
        
        return result
    

    def _print_summary_table(self, summary):
        """以表格形式打印摘要（保留6位小数）"""
        lines = []
        lines.append("统计摘要:")
        lines.append("")
    
        # 表头
        header = f"{'Metric':<12} {'Jaccard':<12} {'ANI':<12}"
        lines.append(header)
        lines.append("-" * len(header))
    
        # 数据行
        metrics = ['min', 'max', 'mean', 'median']
        for m in metrics:
            j_val = summary['jaccard'][m]
            j_str = f"{j_val:.6f}"
            if 'ani' in summary:
                ani_val = summary['ani'][m]
                ani_str = f"{ani_val:.4f}"
            else:
                ani_str = "N/A"
            lines.append(f"{m.capitalize():<12} {j_str:<12} {ani_str:<12}")
    
        # 输出每一行
        for line in lines:
            self.console.print_info(line)

    
    def _output_results(self):
        """输出结果"""
        if not self.results:
            self.console.print_warning("没有满足条件的结果")
            return
        
        # 按Jaccard指数排序
        self.results.sort(key=lambda x: x.jaccard_index, reverse=True)
        
        # 输出到控制台
        print()
        self.console.print_results(self.results, self.args.format)
        print()
        
        # 输出到文件
        if self.args.output:
            writer = FileWriter(self.args.output, self.console)
            writer.write_results(self.results, self.args.format)
        
        # 输出摘要
        if self.args.verbose:
            summary = OutputFormatter.format_summary(self.results)
            self._print_summary_table(summary)


def main():
    """主函数"""
    try:
        # 解析参数
        args = parse_arguments()
        
        # 创建并运行主程序
        app = GenomeSimilarity(args)
        app.run()
        
    except KeyboardInterrupt:
        sys.stderr.write("\n用户中断\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"程序错误: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()