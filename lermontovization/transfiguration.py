import logging
import sys
import pymorphy2
from preprod_research.tag_id_dict import shaping_grammemes, redundant_grammemes, pos_of_interest


logger = logging.getLogger(__name__)
logger.debug(sys.executable)


logger = logging.getLogger(__name__)

import re

MORPH = pymorphy2.MorphAnalyzer()
INSANE = MORPH.parse('безумный')[0]
UNWORLDY = MORPH.parse('неземной')[0]
UNEARTHLY = MORPH.parse('неотмирен')[0]  # Вспомогательный эпитет, используемый в качестве краткой формы второго эпитета
EPITHETS = [INSANE, UNWORLDY]

# регулярка для поиска слов
WORD_RE_COMPILED = re.compile(r'\w+')

# TODO: предусмотреть в коде, что pymorphy может вернуть не единственный вариант разбора слова:
'''
pymorphy2 возвращает все допустимые варианты разбора, но на практике обычно нужен только один вариант, правильный.

У каждого разбора есть параметр score:

>>> morph.parse('на')
[Parse(word='на', tag=OpencorporaTag('PREP'), normal_form='на', score=0.999628, methods_stack=((<DictionaryAnalyzer>, 'на', 23, 0),)),
 Parse(word='на', tag=OpencorporaTag('INTJ'), normal_form='на', score=0.000318, methods_stack=((<DictionaryAnalyzer>, 'на', 20, 0),)),
 Parse(word='на', tag=OpencorporaTag('PRCL'), normal_form='на', score=5.3e-05, methods_stack=((<DictionaryAnalyzer>, 'на', 21, 0),))]
'''

#TODO: предусмотреть работу с наречиями Parse(word='чисто', tag=OpencorporaTag('ADVB')


def transfigurate_given_word(word, epithet_num=0):
    print('---' * 30)

    word_parse = MORPH.parse(word)
    for p in word_parse:
        if p.tag.POS in pos_of_interest:
            tag_str = str(p.tag)
            break
    else:
        print(word)
        print('Часть речи преобразуемого слова должна быть "прилагательное" или  "краткое прилагательное"')
        return None


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

    return epithet.inflect(target_form_grammemes).word


def process_text_line(line, epithet_n=0):
    resulting_line = line
    words_of_line = WORD_RE_COMPILED.findall(line)
    for word in words_of_line:
        transfigurated_word = transfigurate_given_word(word, epithet_num=epithet_n)
        if transfigurated_word is not None:
            resulting_line = resulting_line.replace(word, transfigurated_word, 1)
            epithet_n = 1 - epithet_n
    return resulting_line, epithet_n


def process_text_file(source_text_file_path):
    epithet_n = 0
    source_text_file_path = ('bianki.txt')
    transfigurated_lines = []
    with open(source_text_file_path, 'r') as source_text_file:
        for i, line in enumerate(source_text_file.readlines()):
            transfigurated_line, epithet_n = process_text_line(line, epithet_n)
            transfigurated_lines.append(transfigurated_line)
    return '\n'.join(transfigurated_lines)

print(process_text_line('День немыслимо прекрасен, небо чисто и светло', 0))