# ProteinLoader
## TODO: logo 设计

## 总体思路
设计思路大概是使用通用的流程和尽可能少的依赖完成所需要的内容。

目标是raw data从下载，预处理，到比较著名数据集的预定义版本。最终实现类似下面两行载入数据的效果
```python
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)
```
### 流程步骤

0. 从不同的source批量下载文件
###### 这里有疑问
大概思路是与定义yaml文件写入在哪下载之类的信息。然后所需要的预处理步骤也可以在这里定义好

1. 从不同的文件format读取并进行初步清洗，统一使用pandas.dataframe作为中间格式
主要目标是通过数据清理统一格式： 这可能包括诸如删除缺失的氨基酸残基、去除不完整或错误的条目、删除异常值等步骤。
###### 这里有疑问
dataframe的好处在于提供了统一且容易操作的中间格式，同时dataframe容易链接神经网的数据载入。如果使用Anndata可能更好？

目前的设计流程是：

raw -> preprocessor.pfiles.read() -> pandas.dataframe -> preprocessor.pfiles.clean_data() ->pandas.dataframe -> preprocessor.pfiles.dihedral_to_tensor() -> torch.Tensor()

其中preprocessor.pfiles.read()读取不同文件转化为dataframe，涵盖fasta，pdb和mmcif

其中preprocessor.pfiles.clean_data()包含了original部分的get_pdb_singleChain和extract_single_conformation。

这个流程主要是依照original的拆解，但是不太确定是否拆解正确
###### 这里有疑问
网上还找到了如下可能的部分但是不确定是否有关于我们的任务：针对特定需求的蛋白质设计深度学习数据载入包

去除或替换异源物种和非标准残基：PDB中的蛋白质可能包含异源物种或非标准氨基酸残基，这些可能需要在分析之前被去除或替换。
去除水分子和小分子配体：除非特别关心这些分子，否则通常会在进行结构分析之前去除它们。

2. 序列对齐：对于一组蛋白质，可能需要进行序列对齐以确定它们之间的相似性和差异。
###### 这里有疑问
不确定这个是否有必要，列出搜索到的信息

常见的序列对齐方法：

全局对齐：这种方法试图对齐两个序列的全部长度。一个常见的全局对齐算法是 Needleman-Wunsch 算法。
局部对齐：这种方法试图找到两个序列中最佳匹配的子序列，而不一定涉及整个序列。一个常见的局部对齐算法是 Smith-Waterman 算法。
多序列对齐：这种方法试图对齐三个或更多的序列。常见的多序列对齐工具有 ClustalW、MUSCLE、MAFFT 等。
分级聚类：这种方法首先计算所有序列之间的距离，然后将最相似的序列组合在一起，逐步形成一个层次结构。例如，UPGMA (Unweighted Pair Group Method with Arithmetic Mean) 就是一种分级聚类方法。

3. 特征提取：对于机器学习或数据分析，可能需要从蛋白质序列或结构中提取一些特征，例如氨基酸组成、二级结构元素的比例、溶剂可及性、接触数等
###### 这里有疑问
不确定是否有必要，或者有多大的必要关联到深度学习的数据载入部分


4. 标准化或归一化：如果从蛋白质序列或结构中提取特征进行机器学习，可能需要将特征值标准化或归一化
###### 这里有疑问
不确定是否必要，在深度学习常见这个部分，但是对于蛋白质如何进行不清楚

5. dataset预定义
###### 这里有疑问
为了实现类似下面两行载入数据的效果
```python
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)
```
可能需要更清楚的描述都有哪些数据增强被应用了，我在这里比较空白

6. 问答文档部分
###### 这里有疑问
大概是服从什么流程，提供什么作为基本内容。目标是我们问了，模型可以依赖这些文档告诉使用者哪些部分是需要考虑的。可以用GPT生成一部分，但是问题可能要仔细斟酌。同时，一般GPT是不提供某个库的特定实现的，我们提供的文档就要依赖本项目相关。