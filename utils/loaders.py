"""
数据加载模块

提供 YAML / JSON / CSV 文件的读取能力，供测试用例和配置加载使用。
"""

from typing import Any, Dict
import yaml
import json
import csv
from abc import ABC, abstractmethod
from pathlib import Path

class DataLoader(ABC):
    """数据加载基类"""

    @staticmethod
    def _resolve_path(file_path: str) -> Path:
        """解析文件路径，返回实际存在的绝对路径"""
        p = Path(file_path)
        if p.is_absolute():
            if p.exists():
                return p
            raise FileNotFoundError(f"文件不存在: {p}")

        # 1. 尝试相对于 CWD
        if p.exists():
            return p.resolve()

        # 2. 尝试相对于项目根（loaders.py 的上上级）
        project_root = Path(__file__).parent.parent
        alt = project_root / file_path
        if alt.exists():
            return alt.resolve()

        raise FileNotFoundError(
            f"文件不存在: {file_path}\n"
            f"尝试过:\n"
            f"  CWD 下: {Path.cwd() / file_path}\n"
            f"  项目根下: {alt.resolve()}"
        )

    @staticmethod
    def _get_suffix(file_path: str) -> str:
        """获取文件后缀（小写，带点）"""
        return Path(file_path).suffix.lower()

    @abstractmethod
    def _do_load(self, file_path: str) -> Any:
        """子类实现具体的加载逻辑"""
        pass

    def load(self, file_path: str) -> Any:
        """
        公共入口：加载数据

        Args:
            file_path (str): 文件路径

        Returns:
            Any: 加载的数据

        Raises:
            FileNotFoundError: 文件不存在时抛出
            ValueError: 文件格式不正确时抛出
        """
        resolved = self._resolve_path(file_path)
        return self._do_load(str(resolved))

class YamlLoader(DataLoader):
    """负责加载 YAML 文件"""
    def _do_load(self, file_path: str) -> Any:
        with open(file_path, mode='r', encoding='utf-8') as f:
            return yaml.safe_load(f)

class JsonLoader(DataLoader):
    """负责加载 JSON 文件"""
    def _do_load(self, file_path: str) -> Any:
        with open(file_path, mode='r', encoding='utf-8') as f:
            return json.load(f)

class CsvLoader(DataLoader):
    """负责加载 CSV 文件"""
    def _do_load(self, file_path: str) -> Any:
        with open(file_path, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

class AutoLoader(DataLoader):
    """根据文件名后缀自动加载数据"""
    _loaders: Dict[str, DataLoader] = {
        ".yaml": YamlLoader(),
        ".yml": YamlLoader(),
        ".json": JsonLoader(),
        ".csv": CsvLoader()
    }

    def _do_load(self, file_path: str) -> Any:
        suffix = self._get_suffix(file_path)
        if suffix not in self._loaders:
            raise ValueError(
                f"不支持的文件格式: {suffix}，"
                f"仅支持: {list(self._loaders.keys())}"
            )
        return self._loaders[suffix].load(file_path)

if __name__ == '__main__':
    loader = AutoLoader()
    data = loader.load('data/login.yaml')
    print(data)  # 输出 YAML 文件的内容