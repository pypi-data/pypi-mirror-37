# -*- coding: utf-8 -*-

import heapq
import itertools
import json
import os
import pickle
import random
import sys

from collections import Iterator
from itertools import chain
from pathlib import Path
from operator import itemgetter

from tqdm import tqdm

from gensim.corpora.dictionary import Dictionary
from bounter import bounter

from komorebi.util import absolute_path, per_chunk, timing
from komorebi.util import DataError

class TextData(Iterator):
    def __init__(self,
                 filename=None, vocab_size=10**5, max_len=None,
                 chunk_size=10**5, delimiter=None, size_mb=4024, pad_symbol='<pad>',
                 start_symbol='<s>', end_symbol='</s>', unknown_symbol='<unk>',
                 filter_on='tf', prune_at=10**10, encoding='utf8',
                 **kwargs):
        """
        This is the object to store text and read them into vocabulary
        indices. The object is an iterable that yields vocabulary indices of the
        tokens in the sentences.
        :param filename: Textfile that contains source sentences.
        :type filename: str
        :param vocab_size: Max no. of words to keep in the source vocab.
        :type vocab_size: int
        :param chunk_size: Use to limit no. of sentences to load at a time when populating the vocabulary.
        :type chunk_size: int
        :param delimiter: Delimiter to split on when "tokenizing"
        :type delimiter: str
        :param size_mb: Memory footprint of the bounter object use to count the vocab.
        :type size_mb: int
        :param start_symbol: Start symbol use for padding.
        :type start_symbol: str
        :param end_symbol: End symbol use for padding.
        :type end_symbol: str
        :param unknown_symbol: Unknown symbol for OOV words.
        :type unknown_symbol: str
        :param filter_on: Option to filter on term-freq ('tf') or doc-freq ('df')
        :type filter_on: str
        :param prune_at: *prune_at* parameter used by gensim.Dictionary
        :type prune_at: int
        """

        if 'loadfrom' not in kwargs: # Creating.

            self.filename = filename

            # Check that inputs are not None.
            assert Path(self.filename).exists(), "File {filename} does not exist".format(filename=filename)

            # Initialize encoding.
            self.encoding = encoding

            # Initialize the pad, start, end and unknown symbols.
            self.PAD, self.PAD_IDX = pad_symbol, 0
            self.START, self.START_IDX = start_symbol, 1
            self.END, self.END_IDX = end_symbol, 2
            self.UNK, self.UNK_IDX = unknown_symbol, 3

            # Save the user-specific delimiter
            self.delimiter = delimiter

            # Gensim related attribute to keep the pruning cap.
            self.prune_at = prune_at

            # Save the user-specified source/target vocab size.
            self.vocab_size = vocab_size

            # Populate the source vocabulary.
            print('Creating Vocabulary...', end='\n', file=sys.stderr)
            self.vocab = Dictionary([[start_symbol], [end_symbol], [unknown_symbol]],
                                     prune_at=self.prune_at)
            self.counter = bounter(size_mb=size_mb)
            print('Building source vocab and counter...', end=' ', file=sys.stderr)
            self.populate_dictionary(self.filename, self.vocab,
                                     self.counter, chunk_size)

            # Keep the vocabulary to a max set by user.
            print('Filtering least frequent words in vocab.', end='\n', file=sys.stderr)
            if filter_on == 'tf':
                self.filter_n_least_frequent(self.vocab,
                                             self.counter,
                                             self.vocab_size)
            elif filter_on == 'df':
                self.vocab.filter_extremes(no_below=1, no_above=self.prune_at,
                                               keep_n=self.vocab_size,
                                               keep_tokens=['<pad>', '<s>', '</s>', '<unk>'])

            self.iterable = self._iterate()

        else: # Loading.
            self.load(kwargs['loadfrom'], kwargs.get('load_counter', False))
            self.iterable = self._iterate()


    @timing
    def load(self, loadfrom, load_counter=False):
        """
        The load function.
        :param loadfrom: The path to load the directory for the ParallelData.
        :type loadfrom: str
        :param load_counter: Whether to load the src and trg bounter objects.
        :type load_counter: bool
        """
        config_file = loadfrom + '/TextData.json'
        if not Path(config_file).exists():
            raise DataError('{} config file not found!!'.format(config_file))
        else:
            print('Loading TextData from {}'.format(config_file),
                  end=' ', file=sys.stderr)
            with open(config_file) as fin:
                self.__dict__ = json.load(fin)

            with open(self.vocab, 'rb') as fin:
                self.vocab = pickle.load(fin)

            if load_counter:
                if ('counter' not in self.__dict__):
                    raise DataError('TextData counter not found!!')
                with open(self.counter, 'rb') as fin:
                    self.counter = pickle.load(fin)

    @timing
    def save(self, saveto, save_counter=False):
        """
        The save function.
        :param saveto: The path to save the directory for the TextData.
        :type saveto: str
        :param save_counter: Whether to save the bounter objects.
        :type save_counter: bool
        """
        print("Saving TextData to {saveto}".format(saveto=saveto), end=' ', file=sys.stderr)
        # Create the directory if it doesn't exist.
        if not Path(saveto).exists():
            os.makedirs(saveto)
        # Save the vocab files.
        with open(saveto+'/vocab.pkl', 'wb') as fout:
            pickle.dump(self.vocab, fout)

        # Initialize the config file.
        config_json = {'filename': absolute_path(self.filename),
                       'delimiter': self.delimiter, 'encoding': self.encoding,
                       'PAD': self.PAD, 'PAD_IDX': self.PAD_IDX,
                       'START': self.START, 'START_IDX': self.START_IDX,
                       'END': self.END, 'END_IDX': self.END_IDX,
                       'UNK': self.UNK, 'UNK_IDX': self.UNK_IDX,
                       'vocab_size': self.vocab_size,
                       'vocab': absolute_path(saveto+'/vocab.pkl')}

        # Check whether we should save the counter.
        if save_counter:
            with open(saveto+'/counter.pkl', 'wb') as fout:
                pickle.dump(self.counter, fout)

        config_json['counter'] = absolute_path(saveto+'/counter.pkl')

        # Dump the config file.
        with open(saveto+'/TextData.json', 'w') as fout:
            json.dump(config_json, fout, indent=2)

    def split_tokens(self, s):
        """
        A "tokenizer" that splits on space. If the delimiter is set to an empty
        string, it will read characters as tokens.
        :param s: The input string.
        :type s: str
        """
        if self.delimiter == '': # Character models.
            return list(s.strip())
        else: # Word models.
            return s.strip().split(self.delimiter)

    @timing
    def populate_dictionary(self, filename, vocab, counter, chunk_size):
        with open(filename, encoding=self.encoding) as fin:
            for chunk in tqdm(per_chunk(fin, chunk_size)):
                if all(c == None for c in chunk): break;
                chunk_list_of_tokens = [self.split_tokens(s) for s in chunk if s]
                vocab.add_documents(chunk_list_of_tokens, self.prune_at)
                counter.update(chain(*chunk_list_of_tokens))

    def filter_n_least_frequent(self, vocab, counter, n):
        """
        Remove the least frequent items form the vocabulary.
        :param vocab: self.src_vocab or self.trg_vocab
        :type vocab: gensim.Dictionary
        :param counter: self.src_counter or self.trg_counter
        :type counter: bounter
        :param n: The upper limit of how many items to keep in the vocabulary
        :type n: int
        """
        # If n is bigger than user specified size, don't filter anything.
        if n < len(vocab.token2id):
            good_ids = [vocab.token2id[token] for token, _ in
                       sorted(counter.items(), key=itemgetter(1))[-n:]
                       if token in vocab.token2id]
            vocab.filter_tokens(good_ids=good_ids)

    def vectorize_sent(self, sent, vocab, pad_start=True, pad_end=True):
        """
        Vectorize the sentence, converts it into a list of the indices based on
        the vocabulary. This is used by the `variable_from_sent()`.
        :param sent: The input sentence to convert to vocabulary indices
        :type sent: list(str)
        :param vocab: self.src_vocab or self.trg_vocab
        :type vocab: gensim.Dictionary
        :param pad_start: Pad the start with the START_IDX [default: True]
        :type pad_end: bool
        :param pad_end: Pad the start with the END_IDX [default: True]
        :type pad_end: bool
        """
        sent = self.split_tokens(sent) if type(sent) == str else sent
        vsent = vocab.doc2idx(sent, unknown_word_index=self.UNK_IDX)
        if pad_start:
            vsent = [self.START_IDX] + vsent
        if pad_end:
            vsent = vsent + [self.END_IDX]
        return vsent

    def variable_from_sent(self, sent, vocab):
        """
        Create the vocaburly indices given a sentence
        :param sent: The input sentence to convert to vocaburly indices
        :type sent: list(str) or str
        :param vocab: self.src_vocab or self.trg_vocab
        :type vocab: gensim.Dictionary
        """
        sent = self.split_tokens(sent) if type(sent) == str else sent
        vsent = self.vectorize_sent(sent, vocab)
        return vsent

    def unvectorize(self, vector, vocab, unpad_left=True, unpad_right=True):
        """
        Convert the vector to the natural text sentence.
        """
        return ' '.join([vocab[idx] for idx in
                         map(int,chain(*vector))][unpad_left:-unpad_right])

    def reset(self):
        """
        Resets the iterator to the 0th item.
        """
        self.iterable = self._iterate()

    def lines(self):
        """
        The function to iterate through the source and target file.
        """
        with open(self.filename) as fin:
            for line in fin:
                yield line.strip()

    def _iterate(self):
        """
        The helper function to iterate through the source and target file
        and convert the lines into vocabulary indices.
        """
        for line in self.lines():
            sent = self.variable_from_sent(line, self.vocab)
            yield sent

    def __next__(self):
        return next(self.iterable)

    def shuffle(self):
        return iter(sorted(self, key=lambda k: random.random()))

    def batch(self, size=1):
        return itertools.islice
