#!/usr/bin/env python3
# import sys
# import os.path
# from random import randint
import yaml
# from com.kagels.util import logger

# As shown in proto-testa-mundi.v2.yaml, the phonotactics config has been updated to include a 'sets' section that defines the character sets for each class (C, V, T, N). The Phonotactics class has been updated to reflect this new structure. The generate_word_from_sets function in wordgen.py has been updated to take a set_dict argument that contains the character sets for each class, and it uses this set_dict to generate syllables based on the phonotactic structure defined in the config. The main function in wordgen.py has been updated to build the set_dict from the config and pass it to the generate_word_from_sets function when generating words.
# phonotactics:
#   language: "Proto Testa Mundi"
#   structure: "CVC"
#   sets: 
#     C: [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
#     V: ["i","e","a","o","u"]
#     T: []
#     N: []


class Phonotactics:
    def __init__(self, language=None, structure=None, sets=None, yml=None):
        self.language  = language  if language  else yml['language']  if yml else None
        self.structure = structure if structure else yml['structure'] if yml else None
        self.sets      = sets      if sets      else yml['sets']      if yml else None
        self._yml_dict = yml

    @classmethod
    def load_from_yaml(cls, yml):
        return Phonotactics(
            language=yml['language'],
            structure=yml['structure'],
            sets=yml['sets'],
            yml=yml
        )
        
    def update_yml_dict(self):
        self._yml_dict = {
            'language': self.language,
            'structure': self.structure,
            'sets': self.sets
        }
        return self._yml_dict
                    
    def yaml(self):
        return self.update_yml_dict()

