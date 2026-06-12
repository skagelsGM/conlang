#!/usr/bin/env python3
import sys
import os.path
# from random import randint
import yaml
# from com.kagels.util import logger

class Config:

    def load_config_from_file(config_file):
        with open(config_file, 'r') as stream:
            try:
                config_yaml = yaml.load(stream, Loader=yaml.FullLoader)
                return Config(config_yaml)
            except yaml.YAMLError as exc:
                logger.error(APP, exc)

    def __init__(self, yml):
        self.phonotactics = Phonotactics(yml['phonotactics'])

    def get_language(self):
        return self.phonotactic.language
