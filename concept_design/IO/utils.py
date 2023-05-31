class pipeline_config:
    """处理Toml的类。对应pipeline配置"""

    def __init__(self):
        self.config_list = []  # 保存所有的配置信息

    def read(self, filepath):
        """从指定路径读取Toml文件，并将结果保存在self.config_list中。
        如果是pipeline，则每个字典必定包含fn_name和fn_kargs两个元素，其中fn_name是需要调用的方法名称，fn_kargs是参数的字典。
        """
        pass

    def write(self, filepath, config_list):
        """将给定的配置列表写入指定的Toml或json文件中。"""
        pass

    def update_config(self, new_config):
        """更新配置信息，将新的配置信息字典添加到self.config_list中。"""
        pass


class mapper_config:
    """处理json文件的类。对应数据库和下载地址mapper"""

    def __init__(self):
        self.config_list = []  # 保存所有的配置信息

    def read(self, filepath):
        """从指定路径读取json文件，并将结果保存在self.config_list中。
        每个元素都是一个字典，如果是读取mapper，字典包含了数据集和对应下载链接；
        """
        pass

    def write(self, filepath, config_list):
        """将给定的配置列表写入指定的json文件中。"""
        pass

    def update_config(self, new_config):
        """更新配置信息，将新的配置信息字典添加到self.config_list中。"""
        pass




import os
import requests

class Downloader:
    """下载类，用于从给定的URL下载数据并将其保存到本地。"""

    def __init__(self, download_dir):
        """初始化Downloader类"""
        self.download_dir = download_dir

    def download_with_wget(self, url, filename):
        """使用wget下载文件，适合大型文件或数据集下载。"""
        pass

    def download_with_crawler(self, url, filename):
        """使用web爬虫下载文件，适合需要精确下载某些特定文件的情况。"""
        pass