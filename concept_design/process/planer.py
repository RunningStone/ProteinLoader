class PipelinePlanner:
    """PipelinePlanner类，按照从toml文件中读取的处理流程依次调用下载，预处理，生成蛋白质Dataset的处理函数。"""

    def __init__(self, pipeline_config):
        """初始化PipelinePlanner类"""
        self.pipeline_config = pipeline_config

    def execute(self):
        """执行处理流程"""
        pass
