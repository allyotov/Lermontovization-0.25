import pymorphy2

MORPH = pymorphy2.MorphAnalyzer()
LERMONTOVIZATION_EPITHETS = ['безумный', 'неземной', 'безумен', 'неотмирен']


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


epithets_forms_dict = dict()

for epithet in LERMONTOVIZATION_EPITHETS:
    epithets_forms_dict[epithet] = dict()
    word_obj = MORPH.parse(epithet)[0]
    lexeme = word_obj.lexeme

    # print('-' * 40)
    for form in lexeme:
        # print(form.word)
        # print(form.tag)
        epithets_forms_dict[epithet][form.tag] = form.word

epithet_existing_forms = dict()
maximum_possible_forms = set()
for tag_dict in epithets_forms_dict.values():
    maximum_possible_forms |= set(tag_dict.keys())

# print(maximum_possible_forms)

maximum_possible_forms_list = list(maximum_possible_forms)
maximum_possible_forms_list.sort()

for form_tag in maximum_possible_forms_list:
    epithets_form = [epithets_forms_dict[epithet].get(form_tag, '---') for epithet in LERMONTOVIZATION_EPITHETS]
    form_tag_str = (40 - len(str(form_tag))) * ' ' + str(form_tag)
    epithet_form_strs = []
    for epithet_form in epithets_form:
        epithet_form_str = (30 - len(epithet_form)) * ' ' + str(epithet_form)
        epithet_form_strs.append(epithet_form_str)

    print(f'{form_tag_str} '
          f'| {epithet_form_strs[0]} '
          f'| {epithet_form_strs[1]} '
          f'| {epithet_form_strs[2]} '
          f'| {epithet_form_strs[3]} ')

