from preprod_research.tag_id_dict import shaping_grammemes, redundant_grammemes, pos_of_interest
import pymorphy2

MORPH = pymorphy2.MorphAnalyzer()
INSANE = MORPH.parse('безумный')[0]
UNWORLDY = MORPH.parse('неземной')[0]
UNEARTHLY = MORPH.parse('неотмирен')[0]  # Вспомогательный эпитет, используемый в качестве краткой формы второго эпитета
EPITHETS = [INSANE, UNWORLDY]

'''
TODO: предусмотреть в коде, что pymorphy может вернуть не единственный вариант разбора слова:

pymorphy2 возвращает все допустимые варианты разбора, но на практике обычно нужен только один вариант, правильный.

У каждого разбора есть параметр score:

>>> morph.parse('на')
[Parse(word='на', tag=OpencorporaTag('PREP'), normal_form='на', score=0.999628, methods_stack=((<DictionaryAnalyzer>, 'на', 23, 0),)),
 Parse(word='на', tag=OpencorporaTag('INTJ'), normal_form='на', score=0.000318, methods_stack=((<DictionaryAnalyzer>, 'на', 20, 0),)),
 Parse(word='на', tag=OpencorporaTag('PRCL'), normal_form='на', score=5.3e-05, methods_stack=((<DictionaryAnalyzer>, 'на', 21, 0),))]
'''


def transfigurate_given_word(word, epithet_num=0):
    p = MORPH.parse(word)[0]
    print(word)
    tag_str = str(p.tag)
    print(tag_str)

    if p.tag.POS not in pos_of_interest:
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


print(transfigurate_given_word('мокрей'))
