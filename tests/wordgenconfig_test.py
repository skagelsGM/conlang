import pytest

import yaml

from wordgenconfig import Config
# from com.kagels.util.validators import Validator, BooleanValidator, StringValidator, IntegerValidator

from wordgen import load_config_from_file
 
def test_wordgenconfig_hello():
    print("Hello Test World!")
    assert True

# Config yaml v1:
#   language: "Proto Testa Mundi"
#   phonotactics: "CVC"
#   cset: [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
#   vset: ["i","e","a","o","u"]
#   tset: []
#   nset: []
#   C: [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
#   V: ["i","e","a","o","u"]
#   T: []
#   N: []
def test_wordgenconfig_load_config_v1():   
    config = load_config_from_file('./proto-testa-mundi.v1.yaml')
    print(config['phonotactics'])
    assert config['language'] == "Proto Testa Mundi"
    assert config['phonotactics'] == "CVC"
    assert config['cset'] == [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    assert config['vset'] == ["i","e","a","o","u"]
    assert config['tset'] == []
    assert config['nset'] == []
    assert config['C'] == [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    assert config['V'] == ["i","e","a","o","u"]
    assert config['T'] == []
    assert config['N'] == []  
    
def test_wordgenconfig_load_config_v2():   
    config = Config.load_config_from_file('./proto-testa-mundi.v2.yaml')
    print(config.phonotactics)
    assert config.phonotactics.language == "Proto Testa Mundi"
    assert config.phonotactics.structure == "CVC"
    assert config.phonotactics.sets['C'] == [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    assert config.phonotactics.sets['V'] == ["i","e","a","o","u"]
    assert config.phonotactics.sets['T'] == []
    assert config.phonotactics.sets['N'] == []
    
def test_wordgenconfig_v2_serdex():
    ### Test Setup
    #   1. build config
    language = "Serdex"
    structure = "CVC"
    cset = [ "p","t","k","q","th" ]
    vset = ["a","e","i","o","u"]
    wordgen_config = Config( yml = {
        'phonotactics': {
            'language': language,
            'structure': structure,
            'sets': {
                'C': cset,
                'V': vset,
                'T': [],
                'N': []
            }
        }
    })
    
    #  2. dump to file
    config_file = './tests/test-config.yaml'
    with open(config_file, 'w') as file:
        yaml.dump(wordgen_config.yaml(), file)
    
    #  3. Assert config loaded from file matches original config
    config = load_config_from_file(config_file)
    print(config.phonotactics)
    assert config.phonotactics.language == language
    assert config.phonotactics.structure == structure
    assert config.phonotactics.sets['C'] == cset
    assert config.phonotactics.sets['V'] == vset
    assert config.phonotactics.sets['T'] == []
    assert config.phonotactics.sets['N'] == []

