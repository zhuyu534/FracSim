"""安装脚本"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="FracSim",
    version="0.1.0",
    author="ZhuYu",
    author_email="1822852048@qq.com",
    description="基于FracMinHash基因组素描算法的细菌基因组相似度估计工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhuyu534/FracSim.git",
    package_dir={"": "fracsim"},
    packages=find_packages(where="fracsim"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fracsim=fracsim.main:main",
        ],
    },
)