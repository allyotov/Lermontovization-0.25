import unittest
import lermontovization.transfiguration as t


class TestWordTransfiguration(unittest.TestCase):
    def test_adjectives(self):
        for original_word, epithet_num, expected_word in [('мокрый', 0, 'безумный'),  # именительный падеж
                                                          ('мокрого', 0, 'безумного'),  # родительный падеж
                                                          ('мокрого', 0, 'безумного'),  # винительный падеж
                                                          ('мокрому', 0, 'безумному'),  # дательный падеж
                                                          ('мокрым', 0, 'безумным'),  # творительный падеж
                                                          ('мокром', 0, 'безумном')]:  # предложный падеж
            with self.subTest():
                self.assertEqual(expected_word, t.transfigurate_given_word(original_word, epithet_num))

    def test_short_adjectives(self):
        for original_word, epithet_num, expected_word in [('мокр', 0, 'безумен'),
                                                          ('мокр', 1, 'неотмирен')]:
            with self.subTest():
                self.assertEqual(expected_word, t.transfigurate_given_word(original_word, epithet_num))

    def test_comparative(self):
        # COMP, компаратив
        for original_word, epithet_num, expected_word in [('мокрее', 0, 'безумнее'),
                                                          ('мокрее', 1, 'неземнее')]:
            with self.subTest():
                self.assertEqual(expected_word, t.transfigurate_given_word(original_word, epithet_num))

    def test_comparative_v_ej(self):
        # COMP V-ej сравнительная степень на "-ей"
        for original_word, epithet_num, expected_word in [('мокрей', 0, 'безумней'),
                                                          ('мокрей', 1, 'неземней')]:
            with self.subTest():
                self.assertEqual(expected_word, t.transfigurate_given_word(original_word, epithet_num))

    def test_comparative_cmp2(self):
        # COMP Cmp2 сравнительная степень на "по -"
        for original_word, epithet_num, expected_word in [('помокрее', 0, 'побезумнее')]:
            with self.subTest():
                self.assertEqual(expected_word, t.transfigurate_given_word(original_word, epithet_num))

    def test_comparative_cmp2_vej(self):
        # COMP Cmp2 сравнительная степень на "по-" и на "-ей"
        for original_word, epithet_num, expected_word in [('помокрей', 0, 'побезумней')]:
            with self.subTest():
                self.assertEqual(expected_word, t.transfigurate_given_word(original_word, epithet_num))

    def test_unknown_pos_words(self):
        # TODO:('мокрa', 0, 'безумна')]:  # мокра - слово неизвестно pymorphy
        pass

    def test_line_transfiguration(self):
        for original_line, epithet_n, expected_line, expected_epithet_n in \
                [('День немыслимо прекрасен, небо чисто и светло', 0,
                  'День немыслимо безумен, небо неотмирно и безумно', 1),
                 ('День немыслимо прекрасен, небо чисто и светло', 1,
                  'День немыслимо неотмирно, небо безумно и неотмирно', 0)]:
            with self.subTest():
                self.assertEqual((expected_line, expected_epithet_n), t.process_text_line(original_line, epithet_n))
