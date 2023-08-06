# -*- coding: UTF-8 -*-
import yaml


class ConfigParser(object):

    @classmethod
    def __init__(cls, config_file):
        cls.config_file = config_file
        cls.configs = yaml.load(open(cls.config_file, 'r'))


    @classmethod
    def get_config(cls, section=None, key=None):
        '''
        section: 指定一类配置文件, 如mysql 连接信息

        key: 指定section 的同时指定key 获取对应section 下的key 值
        '''
        if not cls.configs:
            cls.configs = yaml.load(open(cls.config_file, 'r'))
        section_configs = cls.configs.get(section, None)
        if section_configs is None:
            raise NotImplementedError

        if not key:
            return section_configs
        else:
            value = section_configs.get(key, None)
        if value is None:
            raise NotImplementedError
        return value
