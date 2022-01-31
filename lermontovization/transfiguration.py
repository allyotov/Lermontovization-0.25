import logging
from multiprocessing import process
import os
import sys
import pymorphy2
from corpy.udpipe import Model, pprint
from preprod_research.tag_id_dict import shaping_grammemes, redundant_grammemes, pos_of_interest


logger = logging.getLogger(__name__)
logger.debug(sys.executable)


logger = logging.getLogger(__name__)

import re

model_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'preprod_research/russian-syntagrus-ud-2.4-190531.udpipe'))
input_text_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'source_text_sample.txt'))
m = Model(model_path)

MORPH = pymorphy2.MorphAnalyzer()
INSANE = MORPH.parse('безумный')[0]
UNWORLDY = MORPH.parse('неземной')[0]
UNEARTHLY = MORPH.parse('неотмирен')[0]  # Вспомогательный эпитет, используемый в качестве краткой формы второго эпитета
EPITHETS = [INSANE, UNWORLDY]
POETIC_FORMS = {'кратк': 'краток'}

# регулярка для поиска слов
WORD_RE_COMPILED = re.compile(r'\w+')


def transfigurate_given_word(word, udpipe_word_tag, epithet_num=0):
    print('---' * 30)
    
    if word in POETIC_FORMS.keys():
        word = POETIC_FORMS[word]

    word_parse = MORPH.parse(word)
    pprint(word_parse)
    if len(word_parse) > 1 and udpipe_word_tag != 'ADJ':
        print(udpipe_word_tag)
        return None, None

    for p in word_parse:
        if p.tag.POS in pos_of_interest:
            tag_str = str(p.tag)
            break
    else:
        print(word)
        print('Часть речи преобразуемого слова должна быть "прилагательное" или  "краткое прилагательное"')
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

    print('Граммемы: ')
    print('Формы: {};'.format(', '.join(target_form_grammemes)))
    if word_redundant_grammemes:
        print('Не влияющие на форму: {};'.format(', '.join(word_redundant_grammemes)))
    if unexplored_grammemes:
        print('Внимание, слову соответствуют следующие неисследованные автором программы лексеммы:')
        print(', '.join(unexplored_grammemes))

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
            pprint(word)
            if word.id == 0:
                continue

            all_upper = False
            capitalized = False
            if word.form.isupper():
                all_upper = True
            else:
                if word.form[0].isupper():
                    capitalized = True

            epithet, new_word = transfigurate_given_word(word.form, word.upostag, epithet_num=epithet_n)
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
        # result_text += ' '
    return result_text

#print(process_text_line('День немыслимо прекрасен, небо чисто и светло', 0))
#sents = list(m.process("День немыслимо прекрасен, небо чисто и светло. Очерк жизни кратк и ясен: правда побеждает зло. Бледнее стал мой друг беспечный."))

# import inspect

# pprint(sents)
# for sent in sents:
#     #print(dir(sent))
#     for word in sent.words:
#         word.lemma = 'зуд'
#         word.form = 'зудёж'
#         pprint(word)
#         # print(dir(word))
#         # pprint(word.feats)
#         # print(type(word))

#         break
    
#     print(sent.getText())
#     break
# pprint(sents)
print(process_text("День немыслимо прекрасен, небо чисто и светло. Очерк жизни кратк и ясен: правда побеждает зло. Бледнее стал мой друг беспечный."))

#print(process_text_file(input_text_path))