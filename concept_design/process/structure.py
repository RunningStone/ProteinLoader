class ProteinStructPreprocessor:
    """蛋白质结构预处理类，包含所有结构数据的预处理方法。"""

    def __init__(self, protein_data):
        """初始化ProteinStructPreprocessor类"""
        self.protein_data = protein_data

    def remove_non_standard_aa(self):
        """从数据中删除非标准的氨基酸"""
        pass

    def remove_H_tag(self):
        """从数据中删除H标签"""
        pass

    def remove_HOH(self):
        """从数据中删除HOH"""
        pass

    def remove_ligand(self):
        """从数据中删除配体"""
        pass

    def separate_chain(self):
        """分离链"""
        pass

    def feature_extraction(self):
        """对处理后的数据进行特征提取"""
        pass
