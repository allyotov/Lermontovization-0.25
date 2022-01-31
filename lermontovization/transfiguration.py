import logging
import os
import pymorphy2
from corpy.udpipe import Model
from preprod_research.tag_id_dict import shaping_grammemes, redundant_grammemes, pos_of_interest


MORPH = pymorphy2.MorphAnalyzer()
INSANE = MORPH.parse('безумный')[0]
UNWORLDY = MORPH.parse('неземной')[0]
UNEARTHLY = MORPH.parse('неотмирен')[0]  # Вспомогательный эпитет, используемый в качестве краткой формы второго эпитета
EPITHETS = [INSANE, UNWORLDY]
POETIC_FORMS = {'кратк': 'краток'}
UDPIPE_MODEL = 'preprod_research/russian-syntagrus-ud-2.4-190531.udpipe'
DEFAULT_TEXT_SAMPLE = 'source_text_sample.txt'

logger = logging.getLogger(__name__)

model_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', UDPIPE_MODEL))
input_text_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                  '..', 
                                  DEFAULT_TEXT_SAMPLE))
m = Model(model_path)


def transfigurate_given_word(word, udpipe_word_tag, epithet_num=0):
    if word in POETIC_FORMS.keys():
        word = POETIC_FORMS[word]

    word_parse = MORPH.parse(word)
    if len(word_parse) > 1 and udpipe_word_tag != 'ADJ':
        return None, None

    for p in word_parse:
        if p.tag.POS in pos_of_interest:
            tag_str = str(p.tag)
            break
    else:
        logger.debug(word)
        logger.debug('Часть речи преобразуемого слова должна быть "прилагательное" или  "краткое прилагательное"')
        return None, None

    tag_str = tag_str.replace(',', ' ')
    grammemes = tag_str.split()

    target_form_grammemes = []
    word_redundant_grammemes = []
    unexplored_grammemes = []
    for grammem in grammemes:
        if grammem in shaping_grammemes:
            target_form_grammemes.append(grammem)
        elif grammem in redundant_grammemes:
            word_redundant_grammemes.append(grammem)
        else:
            unexplored_grammemes.append(grammem)

    logger.debug('Граммемы: ')
    logger.debug('Формы: %;' % ', '.join(target_form_grammemes))
    if word_redundant_grammemes:
        logger.debug('Не влияющие на форму: %s;' % ', '.join(word_redundant_grammemes))
    if unexplored_grammemes:
        logger.debug('Внимание, слову соответствуют следующие неисследованные автором программы лексеммы:')
        logger.debug(', '.join(unexplored_grammemes))

    target_form_grammemes = set(target_form_grammemes)

    epithet = EPITHETS[epithet_num]
    if p.tag.POS == 'ADJS' and epithet_num == 1:
        epithet = UNEARTHLY

    return (epithet, epithet.inflect(target_form_grammemes).word)


def process_text_file(source_text_file_path):
    with open(source_text_file_path, 'r') as source_text_file:
        lines = source_text_file.readlines()
    text_from_file = '\n'.join(lines)

    return process_text(text_from_file)


def process_text(text_str):
    epithet_n = 0
    sents = list(m.process(text_str))
    result_text = ''
    for sent in sents:
        for word in sent.words:
            if word.id == 0:
                continue

            all_upper = False
            capitalized = False
            if word.form.isupper():
                all_upper = True
            else:
                if word.form[0].isupper():
                    capitalized = True

            epithet, new_word = transfigurate_given_word(word.form, 
                                                         word.upostag, 
                                                         epithet_num=epithet_n)
            if new_word:
                if all_upper:
                    new_word = new_word.upper()
                elif capitalized:
                    new_word = new_word.capitalize()

                epithet_n = 1 - epithet_n
                result_text += new_word
            else:
                result_text += word.form

            if hasattr(word, 'misc'):
                if word.misc == 'SpaceAfter=No':
                    result_text += ''
                else:
                    result_text += ' '
            else:
                result_text += ' '
    return result_text