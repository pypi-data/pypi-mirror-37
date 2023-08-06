"""
配置相关
"""
import sys

try:
    properties = __import__('dophon.properties', fromlist=True)
except:
    properties = __import__('dophon_mq.properties.default_properties', fromlist=True)
finally:
    sys.modules['properties'] = properties
    sys.modules['dophon_mq.properties'] = properties
    sys.modules['dophon_mq.properties.properties'] = properties
    sys.modules['dophon.mq.properties'] = properties
    sys.modules['dophon.mq.properties.properties'] = properties
