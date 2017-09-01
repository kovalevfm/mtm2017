# Process itself
# 1) Dictionary from both English and German news corpora (assume not parallel)
# 2) Dictionary from both English and German opensubs (subset)
# 3) Find the words (n-grams) that are very frequent in both English news and opensubs and
# eliminate them to reduce noise originating for universal words (same for german) ???
# 4) Establish limits for similarities to filter the sentences.
# 5) Filter the sentences
# 6) Join the sentences into a in-domain parallel corpus
import nltk
import argparse
from nltk.util import ngrams


# Generates up-to n-grams of a sentence
def word_grams(words, min, max):
    s = []
    for n in range(min, max+1):
        for ngram in ngrams(words, n):
            s.append(' '.join(str(i) for i in ngram))
    return s


# Does the matching to see if the word exists in vocab
def wordmatch(dct, sent, maxgram):
    score = 0
    grams = word_grams(sent, 1, maxgram)
    n = len(grams)
    for i in grams:
        if i in dct:
            score += 1/n
    return score


# Adjust the binarisation according to the sentence length, because impact of
# out-of-vocab words is higher for shorter sents
def scoreadjust(sent, score, threshold):
    if len(sent) <= 4 and score >= threshold*0.8:
        return 1
    elif len(sent) > 4 and len(sent) < 7 and score >= threshold*0.9:
        return 1
    elif score >= threshold:
        return 1
    else:
        return 0


# Scores both parallel sentences to see if the pair should be included
# scoring is binary
def wordscore(endict, dedict, ensent, desent, threshold, maxgram):
    scoreen = wordmatch(endict, ensent, maxgram)
    scorede = wordmatch(dedict, desent, maxgram)
    return min(scoreadjust(ensent, scoreen, threshold),scoreadjust(desent, scorede, threshold))


# Removes frequent words from sents to decrease noise
def removefrequent(frequent, sent):
    return [item for item in sent if item not in frequent]


# Removes infrequent words from sents to decrease noise
def removeinfrequent(infrequent, sent):
    return [item for item in sent if item in infrequent]


# Actually does the sentence selection based on the calculated scores
def selectsents(enfile, defile, enfreqdict, defreqdict, ensubsdict, desubsdict, filename,
                infrequent, frequent, threshold, maxgram):
    # Get top frequent words from dict
    entop = get_top(enfreqdict, ensubsdict)
    detop = get_top(nltk.FreqDist(defreqdict), nltk.FreqDist(desubsdict))

    mylist = sorted(enfreqdict.items(), key=lambda x: x[1], reverse=True)
    endict_pre = []
    for i in mylist:
        if i[1] > 2:
            endict_pre.append(i[0])
        else:
            break
    mylist = sorted(defreqdict.items(), key=lambda x: x[1], reverse=True)
    dedict_pre = []
    for i in mylist:
        if i[1] > 2:
            dedict_pre.append(i[0])
        else:
            break
    # Generate dictionaries
    endict = [item for item in endict_pre if item not in entop]
    dedict = [item for item in dedict_pre if item not in detop]

    # Initalise file writing
    endomain = open(filename + '.en', 'w', encoding='utf-8')
    dedomain = open(filename + '.pt', 'w', encoding='utf-8')

    # Start reading opened out-of-domain parallel files
    ensent0 = enfile.readline()
    desent0 = defile.readline()
    k = 0
    while ensent0 != '' and desent0 != '':
        # Remove frequent noise words
        if frequent:
            ensent = removefrequent(entop, ensent0.split(' ')[:-1])
            desent = removefrequent(detop, desent0.split(' ')[:-1])
        # Remove infrequent words
        if infrequent:
            ensent = removeinfrequent(endict, ensent)
            desent = removeinfrequent(dedict, desent)
        try:
            if wordscore(endict, dedict, ensent, desent, threshold, maxgram) == 1 and len(ensent) >= 1 and len(desent) >= 1:
                endomain.write(ensent0)
                dedomain.write(desent0)
        except UnboundLocalError:
            if wordscore(endict, dedict, ensent0.split(' ')[:-1], desent0.split(' ')[:-1], threshold,
                         maxgram) == 1:
                endomain.write(ensent0)
                dedomain.write(desent0)
        if k % 1000 == 0:
            print(k)
            endomain.close()
            dedomain.close()
            endomain = open(filename + '.en', 'a', encoding='utf-8')
            dedomain = open(filename + '.pt', 'a', encoding='utf-8')
        k += 1
        ensent0 = enfile.readline()
        desent0 = defile.readline()


# Gets top n of the freqdist, for noise removal purposes
def get_top(freqsin, freqsout):
    # Top 50 from in-domain
    list = sorted(freqsin.items(), key=lambda x: x[1], reverse=True)
    topin = []
    for i in list[:50]:
        topin.append(i[0])
    # Top 50 from out-of-domain
    list = sorted(freqsout.items(), key=lambda x: x[1], reverse=True)
    topout = []
    for i in list[:50]:
        topout.append(i[0])
    # Find noise creating top words
    top = [item for item in topin if item in topout]
    return top


# Gets freqdist from a specified file of tokenized sentences.
def get_freqdict(filename, maxgram):
    f = open(filename, 'r', encoding='utf-8')
    x = f.read()
    tok = []
    for line in x.split('\n'):
        tok += word_grams(line.split(' '), 1, maxgram)
    return nltk.FreqDist(tok)


def print_top(sagedused):
    list = sorted(sagedused.items(), key=lambda x: x[1], reverse=True)
    for i in list[:10]:
        print(i[1],i[0],sep='\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="infrequent", type=bool, default=True,
                        help="Should hapax legomena be removed from scoring")
    parser.add_argument("-f", dest="frequent", type=bool, default=True,
                        help="Should joint frequent words be removed from scoring")
    parser.add_argument("-t", dest="threshold", type=float, default=0.9,
                        help="Define the threshold for including the sentence pair")
    parser.add_argument("-n", dest="maxgram", type=int, default=2,
                        help="Define the maximum n-gram we want to examine")
    args = parser.parse_args()
    # Frequency Dictionaries from in-domain non-parallel corpus
    enfreqdict = get_freqdict('News-Commentary11.en-pt.en.tok', args.maxgram)
    defreqdict = get_freqdict('News-Commentary11.en-pt.pt.tok', args.maxgram)

    # Frequency Dictionaries from out-of-domain parallel corpus
    ensubsdict = get_freqdict('Opensubs.test.en', args.maxgram)
    desubsdict = get_freqdict('Opensubs.test.pt', args.maxgram)

    # Open the subs files
    en = open('OpenSubtitles2016.en-pt.en.tok', 'r', encoding='utf-8')
    de = open('OpenSubtitles2016.en-pt.pt.tok', 'r', encoding='utf-8')
    selectsents(en, de, enfreqdict, defreqdict, ensubsdict, desubsdict, 'new-domain-ngram',
                args.infrequent, args.frequent, args.threshold, args.maxgram)