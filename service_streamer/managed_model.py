# coding=utf-8
# Created by Meteorix at 2019/7/22
from multiprocessing import Process
import os


class ManagedModel(object):
    def __init__(self, gpu_id):
        self.model = None
        self.gpu_id = gpu_id
        self.set_gpu_id(self.gpu_id)

    @staticmethod
    def set_gpu_id(gpu_id=None):
        if gpu_id:
            os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    def init_model(self):
        raise NotImplementedError

    def predict(self, batch):
        raise NotImplementedError
