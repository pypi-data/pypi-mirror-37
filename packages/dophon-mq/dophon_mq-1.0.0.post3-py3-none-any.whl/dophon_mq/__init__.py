# coding: utf-8
import inspect
import re

from dophon_mq.properties import properties
from dophon_mq.function_unit import Producer, Consumer

producer = Producer.producer

consumer = Consumer.consumer

__all__ = [
    'producer', 'consumer', 'ConsumerCenter'
]


class ConsumerCenter:
    """
    消息消费者封装(带自动运行)
    """

    def __init__(self):
        """
        注意!!!!
        重写该类的init方法必须显式执行该类的init方法,否则定义的消息消费将失效
        """
        for name in dir(self):
            item = getattr(self, name)
            if not re.match('__.+__', name) and \
                    callable(item) and \
                    re.match('consumer.<locals>.method.<locals>.*', getattr(getattr(item, '__func__'), '__qualname__')):
                fields = inspect.getfullargspec(item).args
                # 清除自对象参数
                staticmethod(item(*fields))
