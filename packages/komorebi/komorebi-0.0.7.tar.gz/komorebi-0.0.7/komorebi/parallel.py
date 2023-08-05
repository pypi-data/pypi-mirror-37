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

from komorebi.text import TextData
from komorebi.util import absolute_path, per_chunk, timing
from komorebi.util import DataError

class ParallelData(Iterator):
    def __init__(self,
                 src_file=None, trg_file=None,
                 src_vocab_size=10**5, trg_vocab_size=10**5,
                 chunk_size=10**5, delimiter=None, size_mb=4024, pad_symbol='<pad>',
                 start_symbol='<s>', end_symbol='</s>', unknown_symbol='<unk>',
                 filter_on='tf', prune_at=10**10, encoding='utf8',
                 **kwargs):
        """
        This is the object to store parallel text and read them into vocabulary
        indices. The object is an iterable that yields tuples of the vocabulary
        indices, one from the source sentence, another from the target.
        :param src_file: Textfile that contains source sentences.
        :type src_file: str
        :param trg_file: Textfile that contains target sentences.
        :type trg_file: str
        :param src_vocab_size: Max no. of words to keep in the source vocab.
        :type src_vocab_size: int
        :param trg_vocab_size: Max no. of words to keep in the target vocab.
        :type trg_vocab_size: int
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
            print('Creating source TextData...', end='\n', file=sys.stderr)
            self.src_data = TextData(src_file, src_vocab_size, **kwargs)
            print('Creating target TextData...', end='\n', file=sys.stderr)
            self.trg_data = TextData(trg_file, trg_vocab_size, **kwargs)

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
        config_file = loadfrom + '/ParallelData.json'
        if not Path(config_file).exists():
            raise DataError('{} config file not found!!'.format(config_file))
        else:
            print('Loading ParallelData from {}'.format(config_file),
                  end=' ', file=sys.stderr)
            with open(config_file) as fin:
                self.__dict__ = json.load(fin)

            if ('src_data' not in self.__dict__ or
                'trg_data' not in self.__dict__):
                raise DataError('source/target TextData not found!!')

            self.src_data = TextData(loadfrom=self.src_data)
            self.trg_data = TextData(loadfrom=self.trg_data)

    @timing
    def save(self, saveto, save_counter=False):
        """
        The save function.
        :param saveto: The path to save the directory for the ParallelData.
        :type saveto: str
        :param save_counter: Whether to save the src and trg bounter objects.
        :type save_counter: bool
        """
        print("Saving ParallelData to {saveto}".format(saveto=saveto), end=' ', file=sys.stderr)
        # Create the directory if it doesn't exist.
        if not Path(saveto).exists():
            os.makedirs(saveto)
            os.makedirs(saveto+'/src/')
            os.makedirs(saveto+'/trg/')

        self.src_data.save(absolute_path(saveto+'/src/'), save_counter)
        self.trg_data.save(absolute_path(saveto+'/trg/'), save_counter)

        # Initialize the config file.
        config_json = {'src_data': absolute_path(saveto+'/src/'),
                       'trg_data': absolute_path(saveto+'/trg/')}

        # Dump the config file.
        with open(saveto+'/ParallelData.json', 'w') as fout:
            json.dump(config_json, fout, indent=2)

    def reset(self):
        """
        Resets the iterator to the 0th item.
        """
        self.iterable = self._iterate()

    def _iterate(self):
        """
        The helper function to iterate through the source and target file
        and convert the lines into vocabulary indices.
        """
        for src_line, trg_line in zip(self.src_data.lines(), self.trg_data.lines()):
            src_sent = self.src_data.variable_from_sent(src_line, self.src_data.vocab)
            trg_sent = self.trg_data.variable_from_sent(trg_line, self.trg_data.vocab)
            yield src_sent, trg_sent

    def __next__(self):
        return next(self.iterable)

    def shuffle(self):
        return iter(sorted(self, key=lambda k: random.random()))

    def batch(self, size=1):
        return itertools.islice
