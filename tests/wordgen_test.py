import pytest
import yaml
from functools import lru_cache

from wordgenconfig import Config
# from com.kagels.util.validators import Validator, BooleanValidator, StringValidator, IntegerValidator

import wordgen 


def _can_segment_word_by_structure(word, structure, charsets):
    token_choices = [tuple(charsets[symbol]) for symbol in structure]

    @lru_cache(maxsize=None)
    def _matches(word_index, symbol_index):
        if symbol_index == len(token_choices):
            return word_index == len(word)

        for token in token_choices[symbol_index]:
            if word.startswith(token, word_index) and _matches(word_index + len(token), symbol_index + 1):
                return True
        return False

    return _matches(0, 0)


def _matches_repeated_structure(word, structure, charsets, syllable_count):
    return _can_segment_word_by_structure(word, structure * syllable_count, charsets)

def test_wordgen_hello():
    print("Hello Test World!")
    assert True
    
def test_config_v1_get_charsets():   
    language = "Proto Testa Mundi"
    structure = "CVC"
    cset = [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    vset = ["i","e","a","o","u"]
    
    config = wordgen.load_config_from_file('./proto-testa-mundi.v1.yaml')
    # print(config.get_charsets())
    # assert config.get_language() == language
    # assert config.get_phonotactic_structure() == structure
    # assert config.get_charsets()['C'] == cset
    # assert config.get_charsets()['V'] == vset
    # assert config.get_charsets()['T'] == []
    # assert config.get_charsets()['N'] == []
    
    charsets = wordgen.config_v1_get_charsets(config)
    assert charsets['C'] == cset
    assert charsets['V'] == vset
    # assert charsets['T'] == []
    # assert charsets['N'] == []
    
def test_generate_words_v1():
    language = "Proto Testa Mundi"
    structure = "CVC"
    cset = [ "p","t","k","q","th","v","s","z","sh","zh","ch","x","h","pf","ts","m","n","ng","w","l","y" ]
    vset = ["i","e","a","o","u"]
    
    config = wordgen.load_config_from_file('./proto-testa-mundi.v1.yaml')
    charsets = wordgen.config_v1_get_charsets(config)
    
    words = wordgen.generate_words(
        charsets        = charsets, 
        word_count      = 5,
        syllable_count  = 2, 
        language        = language, 
        phonotactics    = structure
    )
    
    print(words)
    assert len(words) == 5
    assert all(_matches_repeated_structure(w, structure, charsets, syllable_count=2) for w in words)
    
def test_generate_words_v2_from_file_config():
    config_v2 = Config.load_config_from_file('./proto-testa-mundi.v2.yaml')

    words = wordgen.generate_words_v2(config_v2, word_count=5, syllable_count=2)

    assert len(words) == 5
    assert all(
        _matches_repeated_structure(
            w,
            config_v2.get_phonotactic_structure(),
            config_v2.get_charsets(),
            syllable_count=2,
        )
        for w in words
    )


def test_generate_words_v2_complex_phonotactics_structure():
    config_yaml = {
        'version': 'v2',
        'phonotactics': {
            'language': 'Testa Complexa',
            'structure': 'CVNC',
            'charsets': {
                'C': ['p', 't', 'k', 'th'],
                'V': ['a', 'e'],
                'N': ['m', 'n', 'ng'],
            },
        },
    }
    config_v2 = Config(config_yaml)

    words = wordgen.generate_words_v2(config_v2, word_count=10, syllable_count=1)

    assert len(words) == 10
    assert all(
        _matches_repeated_structure(
            w,
            config_v2.get_phonotactic_structure(),
            config_v2.get_charsets(),
            syllable_count=1,
        )
        for w in words
    )
