#!/usr/bin/env python3
import sys
import getopt
# import os.path
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
# Constants
#------------------------------------------------
APP='word-gen'
MAX_SYLLABLES_IN_WORD   = 4
DEFAULT_WORD_COUNT      = 1
DEFAULT_SYLLABLE_COUNT  = 1
DEFAULT_CONFIG_FILE = 'proto-testa-mundi.v1.yaml'


class InlineList(list):
    pass

class PrettyConfigDumper(yaml.SafeDumper):
    pass

def _represent_inline_list(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

PrettyConfigDumper.add_representer(InlineList, _represent_inline_list)


#------------------------------------------------
# functions
#------------------------------------------------

def generate_word(charsets, syllable_count = 0, language = '', phonotactics = 'CV'):
    if syllable_count == 0:
        syllable_count = randint(1, MAX_SYLLABLES_IN_WORD)

    logger.debug(APP, f"Generating {language} Word with {syllable_count} syllables\nphonotactics: {phonotactics} ...")

    word = [syllable_gen_from_charsets(charsets, phonotactics) for _ in range(syllable_count)]
    return ''.join(word)

def generate_words(charsets, word_count, syllable_count, language, phonotactics):
    return [ generate_word( charsets, syllable_count, language, phonotactics ) for _ in range(word_count) ]

# config_v1 helper function
def config_v1_get_charsets(config:dict):
    charset_keys = set( list( config['phonotactics'] ))
    charsets = { k: config[k] for k in charset_keys }
    logger.debug(APP, f"charset_keys: {charset_keys}")
    logger.debug(APP, f"charsets: {charsets}")
    return charsets

# config_v1: generate list of words from config dictionary
def generate_words_v1(config:dict, word_count, syllable_count):
    return generate_words(
        charsets        = config_v1_get_charsets(config),
        word_count      = word_count,
        syllable_count  = syllable_count,
        language        = config['language'],
        phonotactics    = config['phonotactics']
    )

# config_v2: generate list of words from config object
def generate_words_v2(config:Config, word_count, syllable_count):
    return generate_words(
        charsets        = config.get_charsets(),
        word_count      = word_count,
        syllable_count  = syllable_count,
        language        = config.get_language(),
        phonotactics    = config.get_phonotactic_structure()
    )

def rand_from_charset(charset):
    i = randint(0, len(charset)-1)
    pick = charset[i]
    logger.debug(APP, f"char index: {i}, char: {pick}")
    return pick

def generate_syllable(cset, vset, phonotactics):
    set_dict = { 'C': cset, 'V': vset }
    return syllable_gen_from_charsets(set_dict, phonotactics)
    
def syllable_gen_from_charsets(charsets, phonotactics):
    # syllable = list( map(lambda l: exec_syllable_func(l, set_dict), list(phonotactics) ))
    # logger.info(APP, syllable)
    syllable = list( map(lambda l: rand_from_charset(charsets[l]), list(phonotactics) ))
    return ''.join(syllable)

def _format_config_for_printing(node):
    if isinstance(node, dict):
        return {key: _format_config_for_printing(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_format_config_for_printing(value) for value in node]
    return node

def _get_inline_charset_keys(config):
    phonotactics = config.get('phonotactics') if isinstance(config, dict) else None

    if isinstance(phonotactics, str):
        return set(phonotactics)

    if isinstance(phonotactics, dict):
        structure = phonotactics.get('structure')
        if isinstance(structure, str):
            return set(structure)

    return set()

def _format_charsets_inline(node, inline_charset_keys):
    if isinstance(node, dict):
        formatted = {}
        for key, value in node.items():
            if key in inline_charset_keys and isinstance(value, list):
                formatted[key] = InlineList([_format_charsets_inline(item, inline_charset_keys) for item in value])
            else:
                formatted[key] = _format_charsets_inline(value, inline_charset_keys)
        return formatted
    if isinstance(node, list):
        return [_format_charsets_inline(value, inline_charset_keys) for value in node]
    return node

def print_header(word_count, syllable_count, config):
    print('---')
    print(f"""[{APP}] Con-Lang Word Generator
Language: {config['language']}
Config:
""")
    inline_charset_keys = _get_inline_charset_keys(config)
    pretty_config = yaml.dump(
        _format_charsets_inline(_format_config_for_printing(config), inline_charset_keys),
        Dumper=PrettyConfigDumper,
        default_flow_style=False,
        sort_keys=False,
        indent=2,
        width=88,
    ).rstrip()
    print(pretty_config)
    print('---')
    logger.info('word-gen', f"Generating {word_count} words with {syllable_count} syllables ...")

def print_results(words):
    print('---')
    print("Words:")
    print(words)
    print('---')

def load_config_from_file(config_file) -> dict:
    logger.info(APP, f"Loading configuration from {config_file}")
    with open(config_file, 'r') as stream:
        try:
            config_yaml = yaml.load(stream, Loader=yaml.FullLoader)
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
    # ------------------------------------------------
    # parse command line args
    # ------------------------------------------------
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:hp:s:w:", ["config=","help", "phonotactics=", "syllable-count=","word-count="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    # wordgen default args
    wordgen_args = {
        'config_file'   : DEFAULT_CONFIG_FILE,
        'phonotactics'  : None,
        'word_count'    : DEFAULT_WORD_COUNT,
        'syllable_count': DEFAULT_SYLLABLE_COUNT
    }

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "--config"):
            wordgen_args['config_file'] = a # config_file = a
        elif o in ("-p", "--phonotactics"):
            wordgen_args['phonotactics'] = a # phonotactics = a
        elif o in ("-s", "--syllable-count"):
            wordgen_args['syllable_count'] = int(a) # syllable_count = int(a)
        elif o in ("-w", "--word-count"):
            wordgen_args['word_count'] = int(a) # word_count = int(a)
        else:
            assert False, f"Invalid option: {o}"
    
    # ...
    # word_count = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    # syllable_count = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

    # ------------------------------------------------
    # Supports config yaml v1 (flat dictionary)
    # ------------------------------------------------
    config_yaml = load_config_from_file(wordgen_args['config_file'])

    # Override config with command line args if provided
    for key, value in wordgen_args.items():
        if value is not None:
            config_yaml[key] = value

    print_header(wordgen_args['word_count'], wordgen_args['syllable_count'], config_yaml)

    # THIS COULD BE BETTER HANDLED BY A FACTORY FUNCTION THAT RETURNS THE APPROPRIATE CONFIG OBJECT BASED ON THE VERSION SPECIFIED IN THE CONFIG YAML; THIS WOULD ALSO HELP TO ENCAPSULATE THE VERSION-SPECIFIC LOGIC FOR LOADING THE CONFIG AND EXTRACTING THE RELEVANT FIELDS FOR WORD GENERATION
    if config_yaml['version'] == 'v1':
        words = generate_words_v1(config_yaml, config_yaml['word_count'], wordgen_args['syllable_count'])
    else:
        # ------------------------------------------------
        # WARNING:  Assumes v2 for now; may want to validate version in config to make sure it is supported
        #           but that can also be handled in the Config class when loading the config from file
        # ------------------------------------------------
        config_v2 = Config.load_config_from_file(wordgen_args['config_file'])
        words = generate_words_v2(config_v2, config_yaml['word_count'], wordgen_args['syllable_count'])

    print_results(words)