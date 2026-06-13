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
    language = "Proto Testa Mundi"
    phonotactics = "CVC"
    cset = [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    vset = ["i","e","a","o","u"]

    config = load_config_from_file('./proto-testa-mundi.v1.yaml')
    print(config['phonotactics'])
    assert config['language'] == language
    assert config['phonotactics'] == phonotactics
    assert config['C'] == cset
    assert config['V'] == vset
    assert config['T'] == []
    assert config['N'] == []  

def test_wordgen_v1_mixed_charsets():
    language = "Test Rando Mundi"
    phonotactics = "CVNT"
    cset = [ "p","k","q","v","s","z","sh","x","h","pf","ts","w","l","y" ]
    vset = ["i","e","a","o","u"]
    tset = ["t", "th","zh","ch"]
    nset = ["m","n","ng"]
    config = load_config_from_file('./tests/test-rando-mundi.v1.yaml')
    print(config['phonotactics'])
    assert config['language'] == language
    assert config['phonotactics'] == phonotactics
    assert config['C'] == cset
    assert config['V'] == vset
    assert config['T'] == tset
    assert config['N'] == nset
    
def test_wordgenconfig_load_config_v2():
    language = "Proto Testa Mundi"
    structure = "CVC"
    cset = [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    vset = ["i","e","a","o","u"]
    config = Config.load_config_from_file('./proto-testa-mundi.v2.yaml')
    print(config.phonotactics)
    assert config.phonotactics.language == language
    assert config.phonotactics.structure == structure
    assert config.phonotactics.charsets['C'] == cset
    assert config.phonotactics.charsets['V'] == vset
    assert config.phonotactics.charsets['T'] == []
    assert config.phonotactics.charsets['N'] == []
    assert config.phonotactics.get_charset('C') == cset
    assert config.phonotactics.get_charset('V') == vset
    assert config.phonotactics.get_charset('T') == []
    assert config.phonotactics.get_charset('N') == []
    
def test_wordgenconfig_v2_serdex():
    ### Test Setup
    # 1. build test config
    language = "Serdex"
    structure = "CVC"
    cset = [ "p","t","k","q","th" ]
    vset = ["a","e","i","o","u"]
    wordgen_config = Config( yaml = {
        'phonotactics': {
            'language': language,
            'structure': structure,
            'charsets': {
                'C': cset,
                'V': vset,
                'T': [],
                'N': []
            }
        }
    })
    
    # 2. dump to yaml file
    config_file = './tests/test-config.yaml'
    with open(config_file, 'w') as file:
        yaml.dump(wordgen_config.yaml(), file)

    # 3. load test config from file
    config = Config.load_config_from_file(config_file)

    ### Assert loaded config is same as original test config
    
    # 4. Assert config loaded from file matches original config
    print(config.phonotactics)
    assert config.phonotactics.language == language
    assert config.phonotactics.structure == structure
    assert config.phonotactics.charsets['C'] == cset
    assert config.phonotactics.charsets['V'] == vset
    assert config.phonotactics.charsets['T'] == []
    assert config.phonotactics.charsets['N'] == []
    assert config.phonotactics.get_charset('C') == cset
    assert config.phonotactics.get_charset('V') == vset
    assert config.phonotactics.get_charset('T') == []
    assert config.phonotactics.get_charset('N') == []

