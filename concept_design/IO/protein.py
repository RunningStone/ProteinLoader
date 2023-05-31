from abc import ABC, abstractmethod

class ProteinFileBase(ABC):
    """基础蛋白质数据文件类，定义了一些基本的行为，如读取，写入和转换为numpy数组"""

    @abstractmethod
    def read(self, filepath):
        """读取文件"""
        pass

    @abstractmethod
    def write(self, filepath, data):
        """写入文件"""
        pass

    @abstractmethod
    def to_numpy(self):
        """将数据转换为numpy数组"""
        pass

class FastaProteinFile(ProteinFileBase):
    """处理fasta格式的蛋白质数据文件"""

    def read(self, filepath):
        """读取fasta文件"""
        pass

    def write(self, filepath, data):
        """写入fasta文件"""
        pass

    def to_numpy(self):
        """将fasta数据转换为numpy数组"""
        pass

class PDBProteinFile(ProteinFileBase):
    """处理pdb格式的蛋白质数据文件"""

    def read(self, filepath):
        """读取pdb文件"""
        pass

    def write(self, filepath, data):
        """写入pdb文件"""
        pass

    def to_numpy(self):
        """将pdb数据转换为numpy数组"""
        pass

class CIFProteinFile(ProteinFileBase):
    """处理cif格式的蛋白质数据文件"""

    def read(self, filepath):
        """读取cif文件"""
        pass

    def write(self, filepath, data):
        """写入cif文件"""
        pass

    def to_numpy(self):
        """将cif数据转换为numpy数组"""
        pass



class Cohort_meta:
    """数据集meta信息的读取抽象基类，定义了一些基本行为，如从文件中读取ID信息，保存ID信息到文件，以及识别ID类型"""

    def name_mapping(self):
        """预定义名称映射到下载链接的方法"""
        pass

    def read_id(self, filepath):
        """从txt或csv文件中读取蛋白质ID信息"""
        pass

    def write_id(self, filepath, id_list):
        """将给定的蛋白质ID列表保存到txt或csv文件中"""
        pass

    def identify_id_type(self, id_str):
        """识别给定的蛋白质ID的类型"""
        pass