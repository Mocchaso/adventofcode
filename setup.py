from setuptools import setup, find_packages

setup(
    name="adventofcode",  # プロジェクト名（任意）
    version="0.1",
    install_requires=[
        "tqdm"
    ],
    packages=find_packages(where="Python"),  # Pythonディレクトリ内のパッケージを検出
    package_dir={"": "Python"},  # パッケージのルートディレクトリを指定
)