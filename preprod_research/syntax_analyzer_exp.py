# from syntax_analyzer import analyzer
#
# parser = analyzer.Parser()
# print(parser)
# sent = "Я пишу письмо старому другу"
#
# t = parser.parse(sent)
# print(t)
# t[0].display()
# import nltk
# nltk.download('averaged_perceptron_tagger_ru')


# import nltk.corpus
# print(dir(nltk.corpus))
#
# from nltk.corpus import brown
# print(brown.words())
# #
# from nltk.corpus import averaged_perceptron_tagger_ru
# print(averaged_perceptron_tagger_ru.words())

#pip install "git+https://github.com/named-entity/nltk4russian.git#egg=nltk4russian"
from nltk4russian.tagger import PMContextTagger
import nltk4russian

# text = word_tokenize()
import pprint
import ufal.udpipe
from ufal.udpipe import Model, Pipeline, ProcessingError
model = Model.load("russian-syntagrus-ud-2.4-190531.udpipe")
print(model)
tokenizer = model.newTokenizer(model.DEFAULT)

conlluOutput = ufal.udpipe.OutputFormat.newOutputFormat("conllu")

sentence = ufal.udpipe.Sentence()

error = ufal.udpipe.ProcessingError()

text = "День немыслимо прекрасен, небо чисто и светло. Очерк жизни кратк и ясен: правда побеждает зло."

tokenizer.setText(text)
tokenizer.nextSentence(sentence, error)
model.tag(sentence, model.DEFAULT)
model.parse(sentence, model.DEFAULT)
print(conlluOutput.writeSentence(sentence))

print(sentence)

https://corpy.readthedocs.io/en/stable/guides/udpipe.html