class ProteinSeqPreprocessor:
    """蛋白质序列预处理类。用于执行各种蛋白质序列预处理步骤。"""

    def __init__(self, dataframe):
        """初始化ProteinSeqPreprocessor类"""
        self.dataframe = dataframe

    def remove_non_standard_aa(self):
        """从数据集中删除非标准的氨基酸"""
        pass

    def split_dataset(self, test_ratio=0.2):
        """将清洁的数据集分成训练集和测试集"""
        pass

    def add_spaces_for_proT5(self):
        """对于ProT5，在进行分词前先添加空格"""
        pass

    def tokenize_sequences(self):
        """进行蛋白质序列的分词操作"""
        pass
