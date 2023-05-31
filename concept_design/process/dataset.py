from torch.utils.data import Dataset

class DatasetGenerator:
    """数据集生成类，用于从预处理的蛋白质数据生成PyTorch的Dataset实例。"""

    def __init__(self, preprocessed_dataframe):
        """初始化DatasetGenerator类"""
        self.dataframe = preprocessed_dataframe

    def generate(self):
        """生成PyTorch的Dataset实例"""
        pass

from torch.utils.data import Dataset

class ProteinDatasetBase(Dataset):
    """蛋白质Dataset的基类，定义通用方法。"""

    def __init__(self, dataframe):
        """初始化ProteinDatasetBase类"""
        self.dataframe = dataframe

    def __len__(self):
        """返回数据集的大小"""
        pass

    def __getitem__(self, idx):
        """获取指定索引的数据"""
        pass


class ProteinSeqDataset(ProteinDatasetBase):
    """对应序列数据的Dataset类"""

    def __init__(self, dataframe):
        """初始化ProteinSeqDataset类"""
        super().__init__(dataframe)


class ProteinStructDataset(ProteinDatasetBase):
    """对应结构数据的Dataset类"""

    def __init__(self, dataframe):
        """初始化ProteinStructDataset类"""
        super().__init__(dataframe)


"""
不再需要单独定义mixed dataset，可以使用sampler获取ID然后对于seq和structure分别采样
"""