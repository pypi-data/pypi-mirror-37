'''
Make an loadable directory from a word2vec/FastText vectors text file. Supports
archives in tar.gz format, or plain text.

https://fasttext.cc/docs/en/english-vectors.html
'''
from pathlib import Path
import plac
import spacy
import numpy
import tqdm
from spacy.vocab import Vectors


def word2vec2spacy(lang, in_loc, out_dir, *args, **kwargs):
    in_loc = Path(in_loc)
    out_dir = Path(out_dir)
    nlp = spacy.blank(lang)
    with open_file(in_loc):
        header = next(file_)
        n_words, width = header.split()
        n_words = int(n_words)
        width = int(width)
        data = numpy.zeros((n_words, width), dtype='f')
        keys = []
        for i, line in tqdm.tqdm(enumerate(file_), total=n_words):
            word, vector = line.split(' ', 1)
            data[i] = numpy.asarray(vector.split(), dtype='f')
            _ = nlp.vocab[word]
            keys.append(word)
        nlp.vocab.vectors = Vectors(data=data, keys=keys)
    nlp.to_disk(out_dir)


if __name__ == '__main__':
    plac.call(fasttext2spacy)

