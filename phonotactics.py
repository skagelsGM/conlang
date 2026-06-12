#!/usr/bin/env python3
import sys
import os.path
# from random import randint
import yaml
from com.kagels.util import logger

#
# language: "Proto Testa Mundi"
#phonotactics:
# structure: "CVC"
# sets: {
#   C: [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ],
#   V: ["i","e","a","o","u"],
#   T: [],
#   N: []
# }

class Phonotactics:
    def __init__(self, language, structure, sets, yml):
        self.language = language
        self.structure = structure
        self.sets = sets
        self._yml = yml

    @classmethod(cls)
    def load_from_yaml(cls, yml):
        return Phonotactics(yml=yml)
