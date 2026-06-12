#!/usr/bin/env python3
import sys
import getopt
import os.path
from random import randint
import yaml
from com.kagels.util.validators import Validator, BooleanValidator, StringValidator, IntegerValidator
from com.kagels.util import logger
from wordgenconfig import Config

'''
Word Gen Config:
- Language: name of the Con-Lang
- Phonotactics: word structure; defines the rules for constructing valid syllables within the Con-Lang
  - Blueprint for making syllables
  - Example: CV represents a Constant followed by a Vowel
sets of letters and dipthongs are defined for legal syllables  in the Con-Lang
- cset (C): set of Consonants used in the Con-Lang
- vset (V): set of Vowels used in the Con-Lang
- tset (T): set of C and V that may start a word
- nset (N): set of C and V that may end a word

'''

#------------------------------------------------
# functions
#------------------------------------------------
APP='word-gen'
MAX_SYLLABLES_IN_WORD = 4

# PROTO_TESTA_MUNDI_CONFIG = """
# language: Proto Testa Mundi
# phonotactics: 'CVC'
# cset: [p,t,k,q,"'",th,v,s,z,sh,zh,ch,x,h,pf,ts,m,n,ng,w,l,y]
# vset: [i,e,a,o,u]
# tset: []
# nset: []
# """

'''
TODO: Generate word based on phonopytactics for the language
'''
def generate_word(cset, vset, syllable_count = 0, language = '', phonotactics = 'CV'):
    if syllable_count == 0:
        syllable_count = randint(1, MAX_SYLLABLES_IN_WORD)

    logger.debug(APP, "Generating %s Word with %s syllables\nphonotactics: %s ..." % (language, syllable_count, phonotactics))

    word = [generate_syllable(cset, vset, phonotactics) for _ in range(syllable_count)]
    return ''.join(word)

def generate_word_from_sets(set_dict, syllable_count = 0, language = '', phonotactics = 'CV'):
    if syllable_count == 0:
        syllable_count = randint(1, MAX_SYLLABLES_IN_WORD)

    logger.debug(APP, f"Generating {language} Word with {syllable_count} syllables\nphonotactics: {phonotactics} ...")

    word = [create_syllable_from_sets(set_dict, phonotactics) for _ in range(syllable_count)]
    return ''.join(word)

def generate_phono_from_set(set):
    v = randint(0, len(set)-1)
    phono = set[v]
    logger.debug(APP, "set index: %s, phono: %s" % (v, phono))
    return phono

def generate_consonant(cset):
    c = randint(0, len(cset)-1)
    consonant = cset[c]
    logger.debug(APP, "consonant index: %s, consonant: %s" % (c, consonant))
    return consonant

def generate_vowel(vset):
    v = randint(0, len(vset)-1)
    vowel = vset[v]
    logger.debug(APP, "vowel index: %s, vowel: %s" % (v, vowel))
    return vowel

def generate_unrecognized(dummy_arg=None):
    ''' dummy_arg is just to make the function signature consistent with the other generate functions '''
    logger.debug(APP, "Unrecognized phonotactic!!!")
    return ''

SYLLABLE_GEN_KEYS = ['C', 'V'] # 'T', 'N
SYLLABLE_GEN_FUNC = {
    'C': generate_consonant,
    'V': generate_vowel
} #   'T': ? , 'N': ? )

def get_syllable_set(ltr, set_dict):
    return set_dict[ltr] if ltr in set_dict.keys() else None

def get_syllable_func(ltr, func_dict=SYLLABLE_GEN_FUNC):
    return func_dict[ltr] if ltr in func_dict.keys() else generate_unrecognized

def exec_syllable_func(ltr, set_dict, func_dict=SYLLABLE_GEN_FUNC):
    set = get_syllable_set(ltr, set_dict)
    gen_func = get_syllable_func(ltr, func_dict)
    return gen_func(set)

def generate_syllable(cset, vset, phonotactics):
    set_dict = { 'C': cset, 'V': vset }
    return create_syllable_from_sets(set_dict, phonotactics)
    
def create_syllable_from_sets(set_dict, phonotactics):    
    syllable = list( map(lambda l: exec_syllable_func(l, set_dict), list(phonotactics) ))                
    # logger.info(APP, syllable)
    return ''.join(syllable)

def print_header(word_count, syllable_count, config):
    print('---')
    print("""[%s] Con-Lang Word Generator
Language: %s
Config:
%s
""" % (APP, config['language'], yaml.dump(config, default_flow_style=True, default_style='', explicit_start=False, explicit_end=False)))
    print('---')
    logger.info('word-gen', "Generating %d words with %d syllables ..." % (word_count, syllable_count))

def print_results(words):
    print('---')
    print("Words:")
    print(words)
    print('---')

def load_config_from_file(config_file):
    logger.info(APP, f"Loading configuration from {config_file}")
    with open(config_file, 'r') as stream:
        try:
            config_yaml = yaml.load(stream, Loader=yaml.FullLoader)
            phonotactics = config_yaml.get('phonotactics') if isinstance(config_yaml, dict) else None
            if isinstance(phonotactics, dict) and {'language', 'structure', 'sets'} <= set(phonotactics.keys()):
                return Config(config_yaml)
            return config_yaml
        except yaml.YAMLError as exc:
            logger.error(APP, exc)
            raise

def usage():
    print("wordgen.py -pswc --phonotactics= --syllable-count= --word-count= --config=")

#------------------------------------------------
# main
#------------------------------------------------
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:hp:s:w:", ["config=","help", "phonotactics=", "syllable-count=","word-count="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    config_file='proto-testa-mundi.v1.yaml'
    phonotactics = None
    word_count = 1
    syllable_count = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "--config"):
            config_file = a
        elif o in ("-p", "--phonotactics"):
            phonotactics = a
        elif o in ("-s", "--syllable-count"):
            syllable_count = int(a)
        elif o in ("-w", "--word-count"):
            word_count = int(a)
        else:
            assert False, "unhandled option"
    
    # ...
    # word_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    # syllable_count = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

    # load config
    # logger.debug(APP, f"Loading configuration from {PROTO_TESTA_MUNDI_CONFIG}")
    # config = yaml.load(PROTO_TESTA_MUNDI_CONFIG, Loader=yaml.FullLoader)
    config = load_config_from_file(config_file)

    if phonotactics is not None:
        config['phonotactics'] = phonotactics

    print_header(word_count, syllable_count, config)

    # TODO: Customize phonotactic classes and their character sets instead of hard-coding for C and V. User should be able to define any class and its set of characters.
    #  - To build the set dict, we can iterate through the phonotactic string and add any classes we encounter to the set dict with their corresponding character sets from the config. This way we can support any number of classes and not just C and V.
    # build set dict from config
    set_dict = { 'C': config['cset'], 'V': config['vset'] }
    # logger.debug(APP, f"set_dict: {set_dict}")   

    # generate words
    # words = [ generate_word(config['cset'], config['vset'], syllable_count, config['language'], config['phonotactics']) for _ in range(word_count)]
    words = [ generate_word_from_sets(set_dict, syllable_count=syllable_count, language=config['language'], phonotactics=config['phonotactics']) for _ in range(word_count)]

    print_results(words)
