import spacy
import nltk
from nltk.corpus import wordnet

#nltk.download('wordnet')
SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]

nlp = spacy.load('en')

def tokenize_sentence(sentence1):
    doc1 = nlp(sentence1)
    sub1_toks = [tok for tok in doc1 if tok.dep_ in OBJECTS or tok.pos_ == "NOUN"]
    
    #doc2 = nlp(sentence2)
    #sub2_toks = [tok for tok in doc2 if tok.dep_ in OBJECTS or tok.pos_ == "NOUN"]
    
    return sub1_toks
    #return (sub1_toks, sub2_toks)
    
def sentence_closeness(sub1_toks, sub2_toks):
    counter = 0
    scores = []
    
    for s1 in sub1_toks:
        for s2 in sub2_toks:
            if str(s1) == "I" or str(s2) == "I":
                continue
            syns = wordnet.synsets(str(s1))
            syns2 = wordnet.synsets(str(s2))
            if len(syns) == 0 or len(syns2) == 0:
                continue
            scores.append(wordnet.synset(syns[0].name()).wup_similarity(wordnet.synset(syns2[0].name())))
            counter += 1

    scores.sort(reverse=True)
    return sum(scores[:min(3, len(scores))])/min(3, len(scores))

#t11,t12 = (tokenize_sentence("I saw an elephant. It was a really cool day. I wouldn't reccomend going on a safari though."), tokenize_sentence("I saw an elephant when I went on a trip to in Africa! I didn't go on a safari though. Good to know that I didn't miss much"))
#t21,t22 = (tokenize_sentence("I saw an elephant. It was a really cool day. I wouldn't reccomend going on a safari though."), tokenize_sentence("I love tacos. While lots of different foods are good, there's something about tacos that just hits the spot every time."))
#t31,t32 = (tokenize_sentence("Today is taco tuesday! But sadly, I could only find burriots around."), tokenize_sentence("I love tacos. While lots of different foods are good, there's something about tacos that just hits the spot every time."))
#  
#print(sentence_closeness(t11,t12))
#print(sentence_closeness(t21,t22))
#print(sentence_closeness(t31,t32))

# Produces the following output:
#   0.9565217391304347
#   0.4895104895104896
#   0.7999999999999999
