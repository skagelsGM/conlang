#!/usr/bin/env python3
# import sys
# import os.path
# from random import randint
import yaml

from com.kagels.util import logger
from com.kagels.util.validators import Validator, BooleanValidator, StringValidator, IntegerValidator
from phonotactics import Phonotactics

class Config:
    APP='wordgen-config'

    @staticmethod
    def load_config_from_file(config_file):
        with open(config_file, 'r') as stream:
            try:
                config_yaml = yaml.load(stream, Loader=yaml.FullLoader)
                return Config(config_yaml)
            except yaml.YAMLError as exc:
                logger.error(Config.APP, exc)
                raise
            
    def load_config__from_yaml(self, yaml):
        return Config(yaml)

    def __init__(self, yaml):
        self.phonotactics = Phonotactics.load_from_yaml(yaml['phonotactics'])

    def get_language(self) -> str:
        return str(self.phonotactics.language)

    def get_phonotactic_structure(self) -> str:
        return str(self.phonotactics.structure)

    def get_charsets(self) -> dict:
        return self.phonotactics.charsets

    def yaml(self):
        return { 'phonotactics': self.phonotactics.yaml() }
