import pymorphy2
import tag_id_dict as td

MORPH = pymorphy2.MorphAnalyzer()
LERMONTOVIZATION_EPITHETS = ['безумный', 'неземной', 'неотмирен']


def get_tags_tuple(form):
    if form.tag.POS == 'COMP':
        result = tuple([form.tag._str])
    else:
        tag_list = []
        for att in ['POS', 'gender', 'number', 'case']:
            att_value = getattr(form.tag, att)
            if att_value is not None:
                tag_list.append(att_value)
        result = tuple(tag_list)
    return result


def get_rus_str_from_tag_str(tag_str):
    tag_list = tag_str.replace(',', ' ').split()
    return ', '.join([td.id_to_rus[id] for id in tag_list])


def get_shape_and_not_meaningful_grammemes(tag_str):
    tag_str = tag_str.replace(',', ' ')
    grammemes = tag_str.split()
    shape_grammemes = []
    not_meaningful_grammemes = []
    for gr in grammemes:
        if gr in td.shape_ids.keys():
            shape_grammemes.append(gr)
        else:
            not_meaningful_grammemes.append(gr)
    return ', '.join(shape_grammemes), ', '.join(not_meaningful_grammemes)


epithets_forms_dict = dict()

for epithet in LERMONTOVIZATION_EPITHETS:
    epithets_forms_dict[epithet] = dict()
    word_obj = MORPH.parse(epithet)[0]
    lexeme = word_obj.lexeme

    for form in lexeme:
        epithets_forms_dict[epithet][form.tag] = form.word

epithet_existing_forms = dict()
maximum_possible_forms = set()
for tag_dict in epithets_forms_dict.values():
    maximum_possible_forms |= set(tag_dict.keys())

maximum_possible_tags_list = list(maximum_possible_forms)
maximum_possible_tags_list.sort()

# To narrow table columns:
# find maximum len of form tag
tag_max_len = max(map(len, map(str, maximum_possible_tags_list)))

# find maximum len of form of each epithet
epithets_max_len = []
for epithet in LERMONTOVIZATION_EPITHETS:
    epithets_max_len.append(max([len(epithets_forms_dict[epithet].get(form_tag, '')) for form_tag in \
                                 maximum_possible_tags_list]))

all_not_meaningfull_in_lexems = set()

for form_tag in maximum_possible_tags_list:
    epithets_form = [epithets_forms_dict[epithet].get(form_tag, '---') for epithet in LERMONTOVIZATION_EPITHETS]
    form_tag_str = (tag_max_len - len(str(form_tag))) * ' ' + str(form_tag)
    epithet_form_strs = []
    for epithet_form, column_width in zip(epithets_form, epithets_max_len):
        epithet_form_str = (column_width - len(epithet_form)) * ' ' + str(epithet_form)
        epithet_form_strs.append(epithet_form_str)

    shape_grammemes, not_meaningful_grammemes = get_shape_and_not_meaningful_grammemes(str(form_tag))
    all_not_meaningfull_in_lexems.update(not_meaningful_grammemes.split(', '))
    shape_str = (35 - len(shape_grammemes)) * ' ' + shape_grammemes
    if not not_meaningful_grammemes:
        not_meaningful_grammemes = '---'
    not_meaningful_gr_str = (20 - len(not_meaningful_grammemes)) * ' ' + not_meaningful_grammemes

    rus_str = get_rus_str_from_tag_str(form_tag_str)
    print(' | '.join([form_tag_str] + epithet_form_strs + [shape_str, not_meaningful_gr_str, rus_str]))
print(all_not_meaningfull_in_lexems)
# из распечатываемой таблицы видно, что эпитеты "безумный" и "безумен" принимают одни и те же формы (морфируются друг в
# друга, краткое прилагательное переходит в исходную форму, если существует). Поэтому "безумен"
# как отдельный эпитет убираем.
# Т.к. у прилагательного "неземной" краткой формы нет, был добавлен синонимичный эпитет "неотмирен", изначально
# у Пригова его не было.
