#!/usr/bin/env python3
import sys
import getopt
import os.path
from random import randint
import yaml
from com.kagels.util import logger

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
TODO: Generate word based on phontactics for the language
'''
def generate_word(cset, vset, syllable_count = 0, language = '', phonotactics = 'CV'):
    if syllable_count == 0:
        syllable_count = randint(1, MAX_SYLLABLES_IN_WORD)

    logger.debug(APP, "Generating %s Word with %s syllables\nphonotactics: %s ..." % (language, syllable_count, phonotactics))

    word = []
    for s in range(syllable_count):
        syllable = generate_syllable(cset, vset, phonotactics)
        # logger.debug(APP,"Syllable index: %s, %s" % (s, syllable))
        word.append(syllable)

    return ''.join(word)

def generate_syllable(cset, vset, phonotactics):
    syllable = []
    for ltr in list(phonotactics):
        logger.debug(APP, "[generate_syllable] Phonotactic: %s" % (ltr))
        if ltr == 'C':
            syllable.append(generate_consonant(cset))
        elif ltr == 'V':
            syllable.append(generate_vowel(vset))
        else:
            logger.debug(APP, "Unrecognized phonotactic!!!")

    # logger.info(APP, syllable
    return ''.join(syllable)

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
    with open(config_file, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            logger.error(APP, exc)

def usage():
    print("wordgen.py -psw --phonotactics= --syllable-count= --word-count= --config=")

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

    config_file='proto-testa-mundi.properties'
    phonotactics = None
    word_count = 1
    syllable_count = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "--config"):
            config_file= a
        elif o in ("-p", "--phonotactics"):
            phonotactics = a
        elif o in ("-s", "--syllable-count"):
            syllable_count = int(a)
        elif o in ("-w", "--word-cound"):
            word_count = int(a)
        else:
            assert False, "unhandled option"
    # ...
    # word_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    # syllable_count = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

    # load config
    # config = yaml.load(PROTO_TESTA_MUNDI_CONFIG, Loader=yaml.FullLoader)
    logger.debug(APP, "Loading configuration from %s" % config_file)
    config = load_config_from_file(config_file)

    if phonotactics is not None:
        config['phonotactics'] = phonotactics

    print_header(word_count, syllable_count, config)

    # TODO: Customize phonotactic classes and their character sets instead of hard-coding for C and V. User should be able to defin any class and its set of characters.

    # generate words
    words = []
    for x in range(word_count):
        word = generate_word(config['cset'], config['vset'], syllable_count, config['language'], config['phonotactics'])
        words.append(word)

    print_results(words)
