# -*- coding:utf-8 -*-


g_global = None

class GlobalData:

    def __init__(self):
        self.configPath = None
        self.targetPath = None
        self.outputPath = None
        self.fileHandler = None

    def create_file_handle(self):
        """
        创建output文件句柄
        :return:
        """
        if self.fileHandler is not None:
            assert False

        if self.outputPath is None:
            return
        else:
            self.fileHandler = open(self.outputPath,"w")

    def close_file_handle(self):
        """
        关闭句柄
        :return:
        """
        if self.fileHandler is None:
            return
        self.fileHandler.close()


def share():
    global g_global
    if g_global is None:
        g_global = GlobalData()
    return g_global