### #IO层：

IO/protein/ Protein: 多个类，定义了读取蛋白质数据的基本行为。有三个文件格式对应三个类实现
IO/protein/ cohort: 数据集meta信息的读取类，可以从txt文件中识别出ID类型并返回类型和一个文件名的list。包含：

IO/utils/
ConfigFile: 处理Toml和json文件的类。描述了pipeline调用和。
Downloader: 下载类，给出下载链接，下载并保存在本地


### Process层：

ProteinSeqPreprocessor: 蛋白序列数据的预处理类。包含各种预处理步骤的方法。
ProteinStructPreprocessor: 结构数据的预处理类。包含所有结构数据的预处理方法。

DatasetGenerator: 数据集生成类，从预处理的蛋白质数据生成PyTorch的Dataset实例。

ProteinDataset: 蛋白Dataset类定义，包括base类定义通用方法，然后分为ProteinSeqDataset, ProteinStructDataset 2个具体实现对应序列，结构形式的数据。同时有结构和序列时候用sampler的方法，只要输入顺序相同即可

### Planning层：

PipelinePlanner: planer 类，按照从toml文件中读取的处理流程依次调用下载，预处理，生成蛋白Dataset的处理函数。