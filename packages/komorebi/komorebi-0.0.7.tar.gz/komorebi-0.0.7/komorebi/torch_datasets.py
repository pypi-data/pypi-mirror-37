# -*- coding: utf-8 -*-

import numpy as np

import torch
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader

from komorebi.parallel import ParallelData

class ParallelDataset(Dataset):
    def __init__(self, src_file, trg_file, max_len):
        # ParallelData object is an iterator packe with goodies =)
        self._data = ParallelData(src_file, trg_file)
        # Iterate through the dataset to get the source and data.
        _source_texts, _target_texts = zip(*self._data)
        self._data.reset() # Resets the iterator to the start.
        # Pre-computes the no. of data points.
        self._len = len(_source_texts)
        self.source_lens = np.clip(list(map(len, _source_texts)), 1, max_len)

        # Converts the indices to torch tensors.
        pad_idx = self._data.src_data.PAD_IDX
        self.source_texts = np.array([self.pad_sequence(_s, max_len, pad_idx)
                                      for _s in _source_texts])
        self.target_texts = np.array([self.pad_sequence(_t, max_len, pad_idx)
                                      for _t in _target_texts])

    def pad_sequence(self, sequence, max_len, pad_idx):
        padded_sequence = np.zeros(max_len, dtype=np.int64)
        padded_sequence[:len(sequence)] = sequence[:max_len]
        if pad_idx != 0:
            padded_sequence[len(x):] = pad_idx
        return padded_sequence

    def __len__(self):
        return self._len

    def __getitem__(self, index):
        return {'x': self.source_texts[index],
                'x_len': self.source_lens[index],
                'y': self.target_texts[index]}

    def batches(self, batch_size, shuffle=True):
        dataloader = DataLoader(dataset=self, batch_size=batch_size, shuffle=shuffle)

        for data_dict in dataloader:
            # Sort indices of data in batch by lengths.
            sorted__indices = np.array(data_dict['x_len']).argsort()[::-1].tolist()
            data_batch = {name:_tensor[sorted__indices]
                          for name, _tensor in data_dict.items()}
            yield data_batch
