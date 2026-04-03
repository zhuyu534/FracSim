"""安装脚本"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="FracSim",
    version="1.0.1",
    author="YuZhu",
    author_email="zhuyu1068@gmail.com",
    description="a FracMinHash-based genome similarity estimator for bacteria",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhuyu534/FracSim.git",
    license="MIT",
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
    python_requires=">=3.8",   # Python3.8引入新的语法海象运算符；与mmh3>=4.0.0兼容良好，可以保证数据类使用的稳定性；Python3.8是一个广泛使用的版本。
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fracsim=fracsim.main:main",
        ],
    },
    zip_safe=False,
)